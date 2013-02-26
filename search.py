# -*- coding: utf-8 -*-
from sys import argv
import re
import json
import requests
from bs4 import BeautifulSoup

def get_similar(soup):
	for item in soup.find_all('div', 'secondaryContent'):
		if item.find('h3', text="Learn More"):
			return [{
			'name': link.text,
			'url': link.get('href')
			} for link in item.find_all('a')]

def get_score(soup):
	return soup.find('span', 'BAscore_big').text

def get_reviews(soup):
	collection = []

	reviews = soup.find('div', attrs={
		'id': 'rating_fullview'
		}).find_all('div', attrs={
		'id': 'rating_fullview_content_2'
		})

	for item in reviews:
		review = {
		'score': item.find('span', 'BAscore_norm').text,
		'text': ' '.join([line.strip() for line in item.strings])
		}
		collection.append(review)

	return collection

def main():
	# URL = argv[1]
	URL = "http://beeradvocate.com/beer/profile/1199/47658"
	r = requests.get(URL)
	soup = BeautifulSoup(r.text)
	print json.dumps(get_similar(soup), indent=4)
	print get_score(soup)
	print json.dumps(get_reviews(soup), indent=4)

if __name__ == '__main__':
	main()
