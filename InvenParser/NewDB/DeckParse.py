from xml.etree.ElementTree import Element, dump
from xml.etree.ElementTree import parse
import re, cgi
import urllib
import json
from datetime import date
from bs4 import BeautifulSoup
import sys
import html2text

def sectionParse(soup,sectionTag):
	codes = ""
	section = soup.find_all('section',sectionTag)[0]
	trs = section.find('tbody').find_all('tr')
	for tr in trs:
		count =  2 if tr['class'][0] == 'even' else 1
		cardID = tr.find('a')['data-id']
		codes += '@' + `int(cardID)` + ':' + `count`
	return codes
		

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
	stop = hotDecks.find('Hearth.HotDecksWidget.initialData.Adventure')
	jsonString = hotDecks[start:stop-6]
	#print jsonString
	data = json.loads(jsonString)
	ids = []
	for deck in data['Decks']:
		ids.append(int(deck['ID']))
	return ids

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
	# parseDeck(1144345)
	hearthpwnDB()
	#hearthpwnDB()

if __name__ == '__main__':
	main()