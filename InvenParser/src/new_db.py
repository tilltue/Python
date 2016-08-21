# -*- coding:utf-8 -*-
from xml.etree.ElementTree import Element, dump
import urllib
import json
from datetime import date
from bs4 import BeautifulSoup
import sys

def stringReplace(string):
    if string != None:
        return string.replace('"','\'')
    else:
        return ""

def cardEngParser(result_cards,urlString):
    print urlString
    #visual-details-cell
    data = urllib.urlopen(urlString)
    soup = BeautifulSoup(data.read(),from_encoding="en-us")
    images = soup.find_all('td','visual-image-cell')
    '''
    for image in images :
        a = image.find('a')
        href = a['href']
        cardCode = href[7:href.find('-')]
        print cardCode
        img = image.find('img')
        src = img['src']
        print src
        engImageSave(src,cardCode)
    '''
    cards = soup.find_all('td','visual-details-cell')
    for card in cards :
    	result_card = {}
    	h3s = card.find_all('h3')
        for h3 in h3s :
            href = h3.find('a')['href']
            cardCode = href[7:href.find('-')]
            result_card['cardCode'] = stringReplace(cardCode)
            cardName = h3.find('a').string
            result_card['cardName'] = stringReplace(cardName)
        lis = card.find_all('li')
        for li in lis :
            if li.contents[0].string == 'Type: ':
            	if li.contents[1].string == 'Minion':
                    cardType = 'minion'
                elif li.contents[1].string == 'Ability':
                    cardType = 'spell'
                elif li.contents[1].string == 'Weapon':
                    cardType = 'weapon'
                result_card['type'] = stringReplace(cardType)
            if li.contents[0].string == 'Class: ':
                result_card['class'] = li.find('a').contents[1].string
            if li.contents[0].string == 'Rarity: ':
            	result_card['rarity'] = li.find('a').string
            if li.contents[0].string == 'Faction: ':
				if li.find('span') != None :
					result_card['faction'] = li.find('span').contents[0].string
            if li.contents[0].string.find('Artist: ') == 0 :
				result_card['artist'] = li.contents[0].string[8:]
        desc = card.find('p')
        if desc != None :
        	cardDesc = ''
        	for i in range(0,len(desc.contents)) :
        		if desc.contents[i].string != None :
        			cardDesc += desc.contents[i].string
        	result_card['desc'] = stringReplace(cardDesc)
        result_card['patch'] = 'Classic'
        result_cards.append(result_card)
    return

def hearthdb():
	resultCards = []
	for i in range(1,4):
		urlString = 'http://www.hearthpwn.com/cards?display=2&filter-premium=1&filter-set=3&filter-unreleased=1&page=%d' % i
		cardEngParser(resultCards,urlString)
	with open('classic_data.json', 'w') as outfile:
		json.dump(resultCards, outfile, indent=4, sort_keys=True, separators=(',', ':'))
	"""
	크툰
    urlString = 'http://www.hearthpwn.com/cards?display=2&filter-premium=1&filter-set=105&filter-unreleased=1&page=2'
    카라잔
    urlString = 'http://www.hearthpwn.com/cards?display=2&filter-premium=1&filter-set=106&filter-unreleased=1&page=1'
    클래식
    http://www.hearthpwn.com/cards?filter-premium=1&filter-set=3&display=2&filter-unreleased=1&page=1    
    for i in range(1,3):
        #urlString = 'http://www.hearthpwn.com/cards?page=%d' % i
        urlString = 'http://www.hearthpwn.com/cards?display=2&filter-set=102&filter-unreleased=1&page=%d' % i
        cardEngParser(f,urlString)
    #urlString = 'http://www.hearthpwn.com/cards?filter-set=100'
        #urlString = 'file:///Users/tilltue/Git/Python/InvenParser/src/test.html'
	"""
    
def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    hearthdb()
    #popularRank()
        
if __name__ == '__main__':
    main()