import requests
from bs4 import BeautifulSoup

from drug import Drug

def get_popular():
	pass

def main():
	base_url = "https://www.drugs.com"
	alpha_url = "/alpha"
	alphabet = "a"
	raw_all_drugs = ""
	for letter in alphabet:
		url = base_url+alpha_url+"/"+letter+"1.html"
		# print(url)
		page = BeautifulSoup(requests.get(url).content, "lxml")
		raw_all_drugs = page.find_all("div", ["boxListPopular"])
	raw_all_drugs = str(raw_all_drugs[0])

	all_drugs = {}
	drug_parsed = BeautifulSoup(raw_all_drugs, "lxml")
	for drug in drug_parsed.find_all("a", href=True):
		all_drugs[drug.string] = Drug(drug.string, base_url+drug["href"])



if __name__ == '__main__':
	main()