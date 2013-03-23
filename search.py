# -*- coding: utf-8 -*-
from sys import argv
from bs4 import BeautifulSoup
import json
import re
import requests
import sqlite3 as sqlite
import time
# import urllib2

profile_re = re.compile(r'\/beer\/profile')
style_re = re.compile(r'\/beer\/style\/')

####
# For crawling the style pages and gathering beer profile URLs:
#
# URL = "http://beeradvocate.com/beer/style"
# seed = gather_urls(URL)
# dump_urls(seed, 'new_urls.txt')
####
def gather_urls(seed):
	r = requests.get(seed)
	soup = BeautifulSoup(r.text)
	urls = []
	styles = ['http://beeradvocate.com' + link.get('href')
		for link in soup.find_all('a')
		if style_re.match(link.get('href'))]
	for url in styles:
		print url
		for link in gather_profiles(url):
			if link not in urls:
				urls.append('http://beeradvocate.com' + link)
	return urls

def gather_profiles(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.text)
	profiles = [link.get('href')
		for link in soup.find_all('a')
		if profile_re.match(link.get('href'))]
	next = soup.find('a', text=re.compile('next ›'))
	if next:
		for link in gather_profiles('http://beeradvocate.com' + next.get('href')):
			if link not in profiles:
				profiles.append(link)
	return profiles

def get_title(soup):
	return soup.find('div', 'titleBar').text.strip()

def get_similar(soup):
	for item in soup.find_all('div', 'secondaryContent'):
		if item.find('h3', text="Learn More"):
			return [{
			'name': link.text,
			'url': 'http://beeradvocate.com' + link.get('href')
			} for link in item.find_all('a')
			if profile_re.match(link.get('href'))]

def get_score(soup):
	return soup.find('span', 'BAscore_big').text

def get_reviews(soup):
	collection = []
	reviews = soup.find_all('div', attrs={
		'id': 'rating_fullview_container'
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
	# In case requests isn't getting it:
	# r = urllib2.urlopen(URL)
	# soup = BeautifulSoup(r.read())
	profile = {
	'name': get_title(soup),
	'url': URL,
	'similar': get_similar(soup),
	'score': get_score(soup),
	'reviews': get_reviews(soup)
	}
	return profile

def load_urls(filename):
	with open(filename, 'rU') as in_file:
		return [line for line in in_file]

def dump_urls(url_list, filename):
	with open(filename, 'w') as out_file:
		out_file.write('\n'.join(url_list))

def crawl_urls(url_list):
	conn = sqlite.connect('reviews.db')
	c = conn.cursor()
	for url in url_list:
		# This is ugly because I don't know of a simple
		# SQLite query with a no-results response.
		c.execute("select * from reviews where url=?", (url,))
		current = c.fetchone()
		if not current:
			print "Fetching ", url
			beer = get_info(url)
			t = (beer['name'], beer['url'], beer['score'], '\n'.join([rev['text'] for rev in beer['reviews']]))
			c.execute("insert into reviews values (?,?,?,?)", t)
			conn.commit()
			# Trying to be polite! Even 1 second is kind of short.
			time.sleep(1)
	conn.close()

def main():
	# When run end-to-end, will scrape all of the
	# beer profile URLs via the beer style pages.
	# Then, it will crawl those profiles and insert
	# the reviews into an SQLite database, reviews.db.
	# seed = 'http://beeradvocate.com/beer/style'
	# urls = gather_urls(seed)

	# This new_urls.txt is a de-duped list of all
	# beer profile URLs, with one URL per line.
	urls = load_urls('new_urls.txt')
	crawl_urls(urls)

if __name__ == '__main__':
	main()
