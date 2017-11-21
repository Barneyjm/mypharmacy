import requests
from bs4 import BeautifulSoup

class Drug(object):
	def __init__(self, name, url):
		self.name = name
		self.url = url
		self.info = self.get_info()

	def get_info(self):
		return BeautifulSoup(requests.get(self.url).content, 'lxml')
