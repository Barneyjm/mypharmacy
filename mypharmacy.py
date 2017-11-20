import requests
from bs4 import BeautifulSoup

def get_popular():
	pass

def main():
	base_url = "https://www.drugs.com"
	alpha_url = "/alpha"
	alphabet = "a"
	for letter in alphabet:
		url = base_url+alpha_url+"/"+letter+"1.html"
		print(url)
		page = BeautifulSoup(requests.get(url).content, "lxml")
		print(page.find_all("div", ["boxListPopular"]))


if __name__ == '__main__':
	main()