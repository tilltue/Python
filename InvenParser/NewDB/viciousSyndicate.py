from xml.etree.ElementTree import Element, dump
from xml.etree.ElementTree import parse
import re, cgi
import urllib
import json
from time import sleep
from datetime import date
from bs4 import BeautifulSoup
import sys
import requests
import html2text

def extract_source(url):
	agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
	source = requests.get(url, headers=agent)
	return source

def syndicate():
	#Hot
	#file = 'hotDeckDB.json'
	#url = "https://www.hearthpwn.com/decks?filter-show-standard=1&filter-show-constructed-only=y&filter-deck-tag=1"
	#Week
	file = 'syndicate.json'
	source = extract_source("https://www.vicioussyndicate.com/deck-library/druid-decks/")
	soup = BeautifulSoup(source.text,from_encoding="en-us")
	print soup

def main():
	reload(sys)
	sys.setdefaultencoding('utf-8')
	#hearthpwnDB()
	#hotDecks()
	syndicate()

if __name__ == '__main__':
	main()