from xml.etree.ElementTree import Element, dump
from xml.etree.ElementTree import parse
import re, cgi
import urllib
import json
from time import sleep
from datetime import date
from bs4 import BeautifulSoup
import sys
import html2text

def sectionParse(soup,sectionTag):
	codes = ""
	sections = soup.find_all('section',sectionTag)
	if len(sections) > 2 :
		section = sections[0]
		trs = section.find('tbody').find_all('tr')
		for tr in trs:
			count =  2 if tr['class'][0] == 'even' else 1
			cardID = tr.find('a')['data-id']
			codes += '@' + `int(cardID)` + ':' + `count`
		return codes
	else:
		return ""
		

def parseDeck(deck_id):
	url = "https://www.hearthpwn.com/decks/%d" % deck_id
	# url = "file:///Users/wade.hawk/Desktop/TEST.htm"
	deckJson = {}
	print(url)
	data = urllib.urlopen(url)
	soup = BeautifulSoup(data.read(),from_encoding="en-us")
	codes = sectionParse(soup,'t-deck-details-card-list class-listing')
	codes += sectionParse(soup,'t-deck-details-card-list neutral-listing')
	author = soup.find_all('section','user-details')[0].find('a')['title']
	deckTitle = soup.find_all('h2','deck-title tip')[0].string
	deckDescription = soup.find_all('div','u-typography-format deck-description')[0]
	markdown = html2text.html2text(deckDescription.prettify())
	deckRating = soup.find_all('div','deck-rating-form')[0].find_all('form','rating-form')[0]['data-rating-sum']
	#print deckDescription.prettify()
	deckJson["title"] = deckTitle
	deckJson["hearthpwnID"] = deck_id
	deckJson["rating"] = deckRating
	deckJson["author"] = author
	deckJson["markdown"] = markdown
	deckJson["codes"] = codes
	return deckJson
	
def popularDecks():
	url = "https://www.hearthpwn.com/"
	# url = "file:///Users/wade.hawk/Desktop/TEST2.htm"
	data = urllib.urlopen(url)
	soup = BeautifulSoup(data.read(),from_encoding="en-us")
	hotDecks = soup.find_all('div','page-block p-base p-base-a t-hot-decks')[0].find_all('script')[1].contents[0].replace('\n','')
	start = hotDecks.find('Hearth.HotDecksWidget.initialData = ') + len('Hearth.HotDecksWidget.initialData = ')
	end = hotDecks.find('Hearth.HotDecksWidget.initialData.Adventure')
	jsonString = hotDecks[start:end-6]
	#print jsonString
	data = json.loads(jsonString)
	ids = []
	for deck in data['Decks']:
		ids.append(int(deck['ID']))
	return ids

def hotDecks():
	#Hot
	#file = 'hotDeckDB.json'
	#url = "https://www.hearthpwn.com/decks?filter-show-standard=1&filter-show-constructed-only=y&filter-deck-tag=1"
	#Week
	file = 'hotDeckWeakDB.json'
	url = "https://www.hearthpwn.com/decks?filter-show-standard=1&filter-show-constructed-only=y&filter-deck-tag=3"
	data = urllib.urlopen(url)
	soup = BeautifulSoup(data.read(),from_encoding="en-us")
	trs = soup.find_all('table','listing listing-decks b-table b-table-a')[0].find('tbody').find_all('tr')
	ids = []
	for tr in trs :
		href = tr.find('td').find('a')['href']
		print href
		start = href.find('decks/') + 6
		end = href[start:].find('-') + start
		ids.append(int(href[start:end]))
	resultDecks = {}
	print len(ids)
	for deck_id in ids[:20] :
		print deck_id
		resultDecks[deck_id] = parseDeck(deck_id)
		sleep(5)
	with open(file, 'w') as outfile:
		json.dump(resultDecks, outfile, indent=4, sort_keys=True, separators=(',', ':'),ensure_ascii=False)

def hearthpwnDB():
	resultDecks = {}
	ids = popularDecks()
	for deck_id in ids :
		print deck_id
		resultDecks[deck_id] = parseDeck(deck_id)
	with open('deckDB.json', 'w') as outfile:
		json.dump(resultDecks, outfile, indent=4, sort_keys=True, separators=(',', ':'),ensure_ascii=False)


def main():
	reload(sys)
	sys.setdefaultencoding('utf-8')
	#hearthpwnDB()
	#hotDecks()
	metaSnapshot()

if __name__ == '__main__':
	main()