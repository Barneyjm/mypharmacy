import requests
from bs4 import BeautifulSoup
import json

class Drug:
	def __init__(self, name, url):
		self.name = name
		self.url = url
		self.overview_page = self.get_overview_page()
		self.overview_questions = {}

		self.get_overview_questions()

	def get_overview_page(self):
		return BeautifulSoup(requests.get(self.url).content, 'lxml')

	def get_overview_questions(self):
		headers = self.overview_page.find_all("h2")
		for head in headers:
			self.overview_questions[head.string] = ""
			nextNode = head
			while True:
				try: 
					nextNode = nextNode.nextSibling
					try:
						tag_name = nextNode.name
					except AttributeError:
						tag_name = ""
					try:
						if tag_name == "p":
							if nextNode.string is None:
								self.overview_questions[head.string] += " " + str(nextNode.text).replace('\n', ' ').replace("\"", "")
							elif nextNode is not None:
								self.overview_questions[head.string] += " " + str(nextNode.string)
						elif tag_name == "ul" or tag_name == "li":
							self.overview_questions[head.string] += " " + str(nextNode.get_text(strip=True))
						elif tag_name == "br":
							print("br!")
							self.overview_questions[head.string] += " " + str(nextNode.get_text(strip=True))
						elif tag_name == "h2":
							break
					except TypeError:
						continue
				except AttributeError:
					break

if __name__ == '__main__':
	abilify = Drug("Acetaminophen", "https://www.drugs.com/acetaminophen.html")
	print(abilify.overview_questions["Acetaminophen dosing information"])

	