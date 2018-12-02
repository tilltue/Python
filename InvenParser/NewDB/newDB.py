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
#MURLOC = 14 DEMON = 15 MECHANICAL = 17 BEAST = 20 TOTEM = 21 DRAGON = 24 PIRATE = 23  ELEMENTAL 18
#rarity enum
#COMMON = 1 FREE = 2 RARE = 3 EPIC = 4 LEGENDARY = 5

tree = parse("./hearthsym/CardDefs.xml")
cardDefRoot = tree.getroot()

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
	raceSet = { '14':'MURLOC', '15':'DEMON', '17':'MECHANICAL', '20':'BEAST', '21':'TOTEM', '24':'DRAGON', '23':'PIRATE','18':'ELEMENTAL' } 
	raceCode = getTagValue(entity,200)
	if raceCode in raceSet :
		cardJson['raceCode'] = raceCode

def getHeroPower(entity,cardJson,heroPowerCardID):
	powerJson = {}
	saveLangText(entity,powerJson,185,'name')
	saveLangText(entity,powerJson,184,'desc')
	powerJson['cost'] = getTagValue(entity,48)
	powerJson['cardClass'] = getTagValue(entity,199)
	powerJson['cardCode'] = entity.attrib['ID']
	cardJson["heroPower"] = powerJson

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

def getElementValue(entity,enumID,element):
	enumString = getEnumTagString(enumID)
	if entity.findall(enumString) :
		text = entity.findall(enumString)[0].attrib['cardID']
		return text
	return ''

def saveLangText(entity,cardJson,enumID,saveTag):
	enumString = getEnumTagString(enumID)
	tag = entity.findall(enumString)
	result = {}
	if len(tag) > 0 :
		for childTag in tag[0].getchildren() :
			result[childTag.tag] = removeTag(childTag.text)
			# if childTag.tag == 'koKR' and saveTag == 'name' :
			# 	print removeTag(childTag.text)
		if len(result) > 0 :
			cardJson[saveTag] = result

def findEntityName(root,name,entity,cardJson,infoJson):
	enumString = getEnumTagString(185)
	tag = entity.findall(enumString)
	cardID = entity.attrib['CardID']
	if cardID[:3] != 'TRL' or 't' not in cardID :
		return None
	if 'TRLA' in cardID :
		return None
	# cardCode = infoJson["cardCode"]
	# if cardID == 'ICC_051t':
	# 	return None
	# if cardID == 'ICC_047t':
	# 	return None
	if len(tag) > 0 :
		if tag[0].getiterator("enUS")[0].text == name :
			collectible = getTagValue(entity,321)
			#if cardSet in ['2','3','4','11','12','13','14','15','20','21','23','25'] :
			#if len(entity.findall("Tag[@enumID='351']")) > 0 :
			if collectible == '1' :
				saveLangText(entity,cardJson,185,'name')
				saveLangText(entity,cardJson,184,'desc')
				saveLangText(entity,cardJson,351,'comment')
				return None
			else :
				print "token"
				saveLangText(entity,cardJson,185,'name')
				saveLangText(entity,cardJson,184,'desc')
				saveLangText(entity,cardJson,351,'comment')
				return entity
	return None

def getCardEntity(root,CardID):
	return root.findall(".//Entity[@CardID='"+CardID+"']")[0]
'''
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
'''

def findOriginalCode(eng_name,infoJson,cardJson,cardType):
	for entity in cardDefRoot.findall(".//Entity") :
		entity = findEntityName(cardDefRoot,eng_name,entity,cardJson,infoJson)
		if entity != None :
			originalCode = entity.attrib['CardID']
			originalID = entity.attrib['ID']
			infoJson['originalID'] = originalID
			infoJson['cost'] = getTagValue(entity,48)
			infoJson['attack'] = getTagValue(entity,47)
			health = getTagValue(entity,45)
			if len(health) == 0 :
				health = getTagValue(entity,187)
			infoJson['health'] = health
			infoJson['rarity'] = getTagValue(entity,203)
			infoJson['cardClass'] = getTagValue(entity,199)
			infoJson['artist'] = getTagText(entity,342)
		 	if getTagValue(entity,482) == '1' :
		 		infoJson['multiClass'] = 'grimy_goons'
		 		print eng_name , 'grimy_goons'
		 	elif getTagValue(entity,483) == '1' :
		 		infoJson['multiClass'] = 'jade_lotus'
		 		print eng_name , 'jade_lotus'
		 	elif getTagValue(entity,484) == '1' :
		 		infoJson['multiClass'] = 'kabal'
		 		print eng_name , 'kabal'
		 	if cardType == 'playableHero' :
		 		heroPowerCardID = getElementValue(entity,380,'cardID')
		 		powerEntity = getCardEntity(cardDefRoot,heroPowerCardID)
		 		infoJson['health'] = getTagValue(entity,292)
		 		getHeroPower(powerEntity,infoJson,heroPowerCardID)
		 	getRace(entity,infoJson)
			cardJson['info'] = infoJson
			return originalCode

def makeHeroPower(power_ids):
	pwnJson = {}
	for power_id in power_ids :
		infoJson = {}
		powerEntity = getCardEntity(cardDefRoot,power_id)
		getHeroPower(powerEntity,infoJson,power_id)
		print infoJson
		info = {}
		info["info"] = infoJson
		pwnJson[power_id] = info
	with open('newDB.json', 'w') as outfile:
		json.dump(pwnJson, outfile, indent=4, sort_keys=True, separators=(',', ':'),ensure_ascii=False)

def cardEngParser(result_cards,urlString,type):
	print urlString
	#visual-details-cell
	data = urllib.urlopen(urlString)
	soup = BeautifulSoup(data.read(),from_encoding="en-us")
	images = soup.find_all('td','visual-image-cell')
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
			# print cardCode + ' ' + cardName
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
				elif li.contents[1].string == 'Playable Hero':
					cardType = 'playableHero'
				else :
					saveCard = False
				infoJson['type'] = stringReplace(cardType)
			if li.contents[0].string == 'Faction: ':
				if li.find('span') != None :
					infoJson['faction'] = li.find('span').contents[0].string
		if saveCard == True :
			cardJson = {}
			if cardName == 'Weaponized Pinata' :
				cardName = 'Weaponized Piñata'
			originalCode = findOriginalCode(cardName,infoJson,cardJson,cardType)
			if originalCode != None :
				cardJson['setType'] = type
				result_cards[originalCode] = cardJson
			else :
				print cardName
	print len(result_cards)
	return

def setTypeDB(filterSet,type,pageCount):
	result_cards = {}
	#정규
	# url = 'http://www.hearthpwn.com/cards?filter-premium=1&filter-set=%d&display=2&filter-unreleased=1' % filterSet
	#토큰
	url = 'http://www.hearthpwn.com/cards?filter-premium=0&filter-set=%d&display=2&filter-unreleased=0&filter-token=1' % filterSet
	# url = 'http://www.hearthpwn.com/cards?filter-name=Stegodon&display=2'
	if pageCount > 0 :
		for i in range(1,pageCount):
			urlString = url + ( '&page=%d' % i )
			cardEngParser(result_cards,urlString,type)
	else :
		cardEngParser(result_cards,url,type)
	writeJson = {}
	writeJson['cards'] = result_cards
	file_name = 'cards_json/%s.json' % type
	with open(file_name, 'w') as outfile:
		json.dump(writeJson, outfile, indent=4, sort_keys=True, separators=(',', ':'),ensure_ascii=False)
		#ensure_ascii=False).encode('utf8') 유니코드로 저장하려면 주석.
	print '%s count: %d' % (type , len(result_cards))

def original():
	setTypeDB(2,'basic',3)
	setTypeDB(3,'classic',4)
	setTypeDB(4,'hallOfFame',0)
	setTypeDB(11,'promo',0)

def hearthpwnDB():
	#original()
	# setTypeDB(100,'naxx',0)
	# setTypeDB(101,'gvsg',3)
	# setTypeDB(102,'blackrock',0)
	# setTypeDB(103,'tgt',3)
	# setTypeDB(104,'loe',0)
	# setTypeDB(105,'oldgod',3)
	# setTypeDB(106,'karazhan',0)
	# setTypeDB(107,'gadgetzan',3)
	# setTypeDB(108,'ungoro',3)
	# setTypeDB(109,'frozen',3)
	# setTypeDB(110,'kobolds',3)
	# setTypeDB(111,'witchwood',3)
	# setTypeDB(113,'boomsday',3)
	setTypeDB(114,'rastakhan',4)	

def loadPwnJson():
	f = open('newDB_backup.json','r')
	pwnJson = json.loads(f.read())
	f.close()
	return pwnJson

def saveRelated(cardJson,originalCode,relatedJson):
	for key in cardJson:
		for card in cardJson[key]:
			infoJson = card.get('info')
			if infoJson != None :
				original = infoJson.get('originalCode')
				print original
				infoJson['test'] = 'a'
				print infoJson
	#관계 카드를 json 데이터에 삽입하려함. info table 에 넣도록 하자.
	
def relatedDB(cardID,originalCode):
	url = 'http://www.hearthhead.com/card=%d' % cardID
	data = urllib.urlopen(url)
	soup = BeautifulSoup(data.read(),from_encoding="en-us")
	scripts = soup.find_all("script")
	pattern = re.compile('var lv_relatedcards = ')
	for script in scripts:
		lv_relatedcards = script.find_all(text=pattern)
		if len(lv_relatedcards) > 0 :
			startIndex = str(script).index('var lv_relatedcards = ') + len('var lv_relatedcards = ')
			endIndex = str(script).index('var lv_emotes = ')
			string = str(script)[startIndex:endIndex]
			string = string.replace(',];',']')
			string = string.replace('];',']')
			print string
			cards = json.loads(string)
			if len(cards) > 0 :
				print card['name']
			#print string
	#cardCdata = soup.find_all(text=re.compile("lv_relatedcards"))

def hearthheadDB():
	#basic
	#getPack()
	pwnJson = loadPwnJson()
	saveRelated(pwnJson,3,3)
	with open('newDB.json', 'w') as outfile:
		json.dump(pwnJson, outfile, indent=4, sort_keys=True, separators=(',', ':'),ensure_ascii=False)
	return
	url = 'http://www.hearthhead.com/cards=?filter=cs=2#text'
	data = urllib.urlopen(url)
	soup = BeautifulSoup(data.read(),from_encoding="en-us")
	cardCdata = soup.find_all(text=re.compile("CDATA"))[2]
	startIndex = cardCdata.index('hearthstoneCards = ') + len('hearthstoneCards = ')
	endIndex = cardCdata.index(';new Listview({')
	cardJson = cardCdata[startIndex:endIndex]
	cardJson = cardJson.replace("popularity","\"popularity\"")
	cards = json.loads(cardJson)
	for card in cards:
		cardID = card['id']
		originalCode = card['image']
		relatedDB(cardID,originalCode)

def main():
	reload(sys)
	sys.setdefaultencoding('utf-8')
	hearthpwnDB()
	#power_ids = ["BOT_238p1","BOT_238p2","BOT_238p3","BOT_238p4","BOT_238p6"]
	#makeHeroPower(power_ids)
	#hearthheadDB()
	#relatedDB(437)
		
if __name__ == '__main__':
	main()