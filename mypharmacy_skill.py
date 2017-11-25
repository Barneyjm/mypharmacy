
# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the My Pharmacy skill. " \
                    "Ask about any popular medicine to learn more about it like, " \
                    "Tell me about advil"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please ask about any popular medicine like, " \
                    "Tell me about advil."
    should_end_session = False

    print(build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session)))

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the My Pharmacy skill. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_drug_attributes(drug):
    return {"drug": drug}


def set_drug_in_session(intent, session): #probably don't need to use this
    """ Sets the drug in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'drug' in intent['slots']:
        drug = intent['slots']['drug']['value']
        drug_info = "Advil is a drug to treat pain."
        session_attributes = create_drug_attributes(drug)
        speech_output = "Here's what I know about " + \
                        drug \
                        drug_info # will be a dynamo db call
        reprompt_text = "You can ask me about any popular medicine like, " \
                        "what's advil?"
    else:
        speech_output = "I'm not sure what that medicine is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what that medicine is. " \
                        "You can ask me about any popular medicine like, " \
                        "what's advil?"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_drug_from_session(intent, session): #get drug from session
    session_attributes = {}
    reprompt_text = None
    card_title = intent['name']
    should_end_session = False

    if 'drug' in intent['slots']:
        drug = intent['slots']['drug']['value']
        drug_info = drug + " is a drug to treat pain."
        session_attributes = create_drug_attributes(drug)
        speech_output = drug_info # will be a dynamo db call
        reprompt_text = "Is there anything else you'd like to know about " + drug
    else:
        speech_output = "I'm not sure what that medicine is. " \
                        "Please try again."
        reprompt_text = "You can ask me about any popular medicine like, " \
                        "what's advil?"

    # if session.get('attributes', {}) and "drug" in session.get('attributes', {}):
    #     drug = session['attributes']['drug']
    #     drug_info = "Advil is a medicine used to treat pain." #dynamodb call
    #     speech_output = "Here's what I know about  " + drug + \
    #                     "." + drug_info
    #     should_end_session = True
    # else:
    #     speech_output = "I'm not sure what that medicine is. " \
    #                     "You can ask me about any popular medicine like, " \
    #                     "what's advil?"
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.

    print(build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session)))
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "MyColorIsIntent": #this'll be the intents i define
        return set_drug_in_session(intent, session)
    elif intent_name == "DrugInfo":
        return get_drug_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

if __name__ == '__main__':
    context = None
    event = {
        'session': {
            'application': {
                'applicationId': '1234'
            },
            'new': True,
            'sessionId': '1234'
        },
        'request': {
            'requestId': '5678',
            'type': 'LaunchRequest',
            'intent': {
                'name': 'DrugInfo',
                'slots': {
                    'drug': {
                        'value': 'Advil'
                        }
                } 
            }            
        }
    }
    #launch test
    lambda_handler(event, context)

    #intent test
    print()
    event['request']['type'] = 'IntentRequest'

    lambda_handler(event, context)