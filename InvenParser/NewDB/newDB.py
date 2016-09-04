# -*- coding:utf-8 -*-
from xml.etree.ElementTree import Element, dump
from xml.etree.ElementTree import parse
import re, cgi
import urllib
import json
from datetime import date
from bs4 import BeautifulSoup
import sys

#class enum
#DRUID = 2 HUNTER = 3 MAGE = 4 PALADIN = 5 PRIEST = 6 ROGUE = 7 SHAMAN = 8 WARLOCK = 9 WARRIOR = 10 NEUTRAL = 12
#race enum
#MURLOC = 14 DEMON = 15 MECHANICAL = 17 BEAST = 20 TOTEM = 21 DRAGON = 24 PIRATE = 23
#rarity enum
#COMMON = 1 FREE = 2 RARE = 3 EPIC = 4 LEGENDARY = 5

langRoots = {}
def getPack():
	lang_pack = ['enUS','deDE','esES','esMX','frFR','koKR','itIT','jaJP','plPL','ptBR','ruRU','zhCN','zhTW','thTH']	
	for lang in lang_pack :
		tree = parse("./locale/"+lang+".xml")
		root = tree.getroot()
		langRoots[lang] = root

def stringReplace(string):
	if string != None:
		return string.replace('"','\'')
	else:
		return ""

def removeTag(string):
	tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')
	string = tag_re.sub('',string)
	string = string.replace('#','')
	string = string.replace('$','')
	string = string.replace('[x]','')
	string = string.replace('\n',' ')
	return string

def getRace(entity,cardJson):
	raceSet = { '14':'MURLOC', '15':'DEMON', '17':'MECHANICAL', '20':'BEAST', '21':'TOTEM', '24':'DRAGON', '23':'PIRATE' } 
	raceCode = getTagValue(entity,200)
	if raceCode in raceSet :
		cardJson['raceCode'] = raceCode

def getHowToEarn(entity,cardJson):
	howtoEarn = getTagText(entity,364)
	howtoEarnGolden = getTagText(entity,365)
	if len(howtoEarn) > 0 :
		cardJson['howToEarn'] = howtoEarn
	if len(howtoEarnGolden) > 0 :
		cardJson['howToEarnGolden'] = howtoEarnGolden

def getEnumTagString(enumID):
	return "Tag[@enumID='%d']" % enumID

def getTagText(entity,enumID):
	enumString = getEnumTagString(enumID)
	if entity.findall(enumString) :
		text = entity.findall(enumString)[0].text
		return removeTag(text)
	return ''

def getTagValue(entity,enumID):
	enumString = getEnumTagString(enumID)
	if entity.findall(enumString) :
		text = entity.findall(enumString)[0].attrib['value']
		return text
	return ''

def findEntityName(root,name,entity):
	nameAttr = getTagText(entity,185)
	if nameAttr == name :
		if len(entity.findall("Tag[@enumID='351']")) > 0 :
			return entity
	return None

def getCardEntity(root,CardID):
	return root.findall(".//Entity[@CardID='"+CardID+"']")[0]

def langPack(lang,CardID,langJson):
	root = langRoots[lang]
	entity = getCardEntity(root,CardID)
	if entity != None :
		textJson = {}
		textJson['desc'] = getTagText(entity,184)
		textJson['comment'] = getTagText(entity,351)
		textJson['cardName'] = getTagText(entity,185)
		getHowToEarn(entity,textJson)
		cardJson = {}
		cardJson['locale'] = lang
		cardJson['text'] = textJson
		#print cardJson
		langJson.append(cardJson)

def findOriginalCode(eng_name,infoJson,cardJson):
	root = langRoots['enUS']
	for entity in root.findall(".//Entity") :
		entity = findEntityName(root,eng_name,entity)
		if entity != None :
			originalCode = entity.attrib['CardID']
			infoJson['originalCode'] = originalCode
			infoJson['cost'] = getTagValue(entity,48)
			infoJson['attack'] = getTagValue(entity,47)
			health = getTagValue(entity,45)
			if len(health) == 0 :
				health = getTagValue(entity,187)
			infoJson['health'] = health
			infoJson['rarity'] = getTagValue(entity,203)
			infoJson['cardClass'] = getTagValue(entity,199)
			infoJson['artist'] = getTagText(entity,342)
			getRace(entity,infoJson)
			langJson = []
			for lang in langRoots.keys() :
				langPack(lang,originalCode,langJson)
			cardJson['lang'] = langJson
			cardJson['info'] = infoJson
			return

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
		infoJson = {}
		saveCard = True
		h3s = card.find_all('h3')
		for h3 in h3s :
			href = h3.find('a')['href']
			cardCode = href[7:href.find('-')]
			infoJson['cardCode'] = stringReplace(cardCode)
			cardName = h3.find('a').string
			#result_card['cardName'] = stringReplace(cardName)
		lis = card.find_all('li')
		for li in lis :
			if li.contents[0].string == 'Type: ':
				if li.contents[1].string == 'Minion':
					cardType = 'minion'
				elif li.contents[1].string == 'Ability':
					cardType = 'spell'
				elif li.contents[1].string == 'Weapon':
					cardType = 'weapon'
				else :
					saveCard = False
				infoJson['type'] = stringReplace(cardType)
			#if li.contents[0].string == 'Class: ':
			#	result_card['class'] = li.find('a').contents[1].string
			#if li.contents[0].string == 'Rarity: ':
			#	result_card['rarity'] = li.find('a').string
			#if li.contents[0].string == 'Race: ':
			#	result_card['race'] = li.find('a').string
			if li.contents[0].string == 'Faction: ':
				if li.find('span') != None :
					infoJson['faction'] = li.find('span').contents[0].string
		"""
			if li.contents[0].string.find('Artist: ') == 0 :
				result_card['artist'] = li.contents[0].string[8:]
		desc = card.find('p')
		if desc != None :
			cardDesc = ''
			for i in range(0,len(desc.contents)) :
				if desc.contents[i].string != None :
					cardDesc += desc.contents[i].string
			result_card['desc'] = stringReplace(cardDesc)
		"""
		if saveCard == True :
			cardJson = {}
			findOriginalCode(cardName,infoJson,cardJson)
			result_cards.append(cardJson)
	print len(result_cards)
	return

def setTypeDB(filterSet,result_cards,type,pageCount):
	cards = []
	url = 'http://www.hearthpwn.com/cards?filter-premium=1&filter-set=%d&display=2' % filterSet
	if pageCount > 0 :
		for i in range(1,pageCount):
			urlString = url + ( '&page=%d' % i )
			cardEngParser(cards,urlString)
	else :
		cardEngParser(cards,url)
	result_cards[type] = cards
	print '%s count: %d' % (type , len(cards))

def original(resultCards):
	setTypeDB(2,resultCards,'basic',3)
	setTypeDB(3,resultCards,'classic',4)
	setTypeDB(4,resultCards,'reward',0)
	setTypeDB(11,resultCards,'promo',0)

def hearthdb():
	resultCards = {}
	#original(resultCards)
	#setTypeDB(100,resultCards,'naxx',0)
	#setTypeDB(101,resultCards,'gvsg',3)
	#setTypeDB(102,resultCards,'blackrock',0)
	#setTypeDB(103,resultCards,'tgt',3)
	#setTypeDB(104,resultCards,'loe',0)
	#setTypeDB(105,resultCards,'oldgod',3)
	setTypeDB(106,resultCards,'karazhan',0)
	with open('newDB.json', 'w') as outfile:
		json.dump(resultCards, outfile, indent=4, sort_keys=True, separators=(',', ':'),ensure_ascii=False).encode('utf8')
		#ensure_ascii=False).encode('utf8') 유니코드로 저장하려면 주석.
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
	getPack()
	hearthdb()
	#popularRank()
		
if __name__ == '__main__':
	main()