# -*- coding: utf-8 -*-
from sys import argv
import re
import json
import requests
from bs4 import BeautifulSoup

def get_title(soup):
	return soup.find('div', 'titleBar').text.strip()

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

def get_info(URL):
	r = requests.get(URL)
	soup = BeautifulSoup(r.text)
	profile = {
	'name': get_title(soup),
	'url': URL,
	'similar': get_similar(soup),
	'score': get_score(soup),
	'reviews': get_reviews(soup)
	}
	return profile

def main():
	# Supply a seed URL or comment the next line
	# and uncomment the second line
	URL = argv[1]
	# URL = "http://beeradvocate.com/beer/profile/1199/47658"
	seed = get_info(URL)
	print json.dumps(seed, indent=4)
	urls = [beer['url'] for beer in seed['similar']]

if __name__ == '__main__':
	main()
