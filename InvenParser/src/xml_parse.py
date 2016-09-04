# -*- coding:utf-8 -*-
import urllib
import json
from datetime import date
from bs4 import BeautifulSoup
import sys
import re, cgi
from xml.etree.ElementTree import parse

tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')

def removeTag(string):
	string = tag_re.sub('',string)
	string = string.replace('#','')
	string = string.replace('$','')
	string = string.replace('[x]','')
	return string

def new_checkHearthPwn():
	tree = parse("enUS.xml")
	root = tree.getroot()
	f_json = open('classic_data.json','rw')
	data = json.loads(f_json.read())
	f_json.close()
	print len(data)
	for card in data :
		name = card['cardName']
		print name
		#print findOriginalCode(root,name)
		result = findOriginalCode(root,name)
		card['originalCode'] = result[0]
		card['desc'] = removeTag(result[1])
		card['comment'] = removeTag(result[2])
		card['artist'] = removeTag(result[3])
		card['attack'] = removeTag(result[4])
		card['health'] = removeTag(result[5])
		card['cost'] = removeTag(result[6])
	with open('newClassic.json', 'w') as outfile:
		json.dump(data, outfile, indent=4, sort_keys=True, separators=(',', ':'))

def checkHearthPwn(root):
    #f_json = open('card_eng.txt','r')
    f_json = open('card_eng_ctun.txt','r')
    data = json.loads(f_json.read())
    f_json.close()
    #print 'check code'+check_code
    print len(data['cards'])
    for card in data['cards'] :
    	name = card['cardName']
    	print name
    	#print findOriginalCode(root,name)
    	result = findOriginalCode(root,name)
    	card['originalCode'] = result[0]
    	card['desc'] = removeTag(result[1])
    	card['comment'] = removeTag(result[2])
    	card['artist'] = removeTag(result[3])
    	card['attack'] = removeTag(result[4])
    	card['health'] = removeTag(result[5])
    	card['cost'] = removeTag(result[6])
    	if unicode('효과') in card :
    		del card[unicode('효과')]
    	if unicode('일러스트') in card :
    		del card[unicode('일러스트')]
    with open('data.json', 'w') as outfile:
    	json.dump(data, outfile, indent=4, sort_keys=True, separators=(',', ':'))
    #print card 
    # for card in data['cards'].length
    # 	print card['cardCode']
    # # for key, value in data.items():
    # 	print key 
    # 	print value
    	# if key == check_code:
     #        #print value
     #        return value
    return #check_code

def findLangPack(root,originalCode):
	for entity in root.findall(".//Entity[@CardID='"+originalCode+"']") :
		nameAttr = entity.findall("Tag[@enumID='185']")[0].text
		descAttr = ''
		comment = ''
		artist = ''
		if entity.findall("Tag[@enumID='184']") :
			descAttr = entity.findall("Tag[@enumID='184']")[0].text
		if entity.findall("Tag[@enumID='351']") :
			comment = entity.findall("Tag[@enumID='351']")[0].text
		return (nameAttr,descAttr,comment)

def findEntity(root,name,entity):
	nameAttr = entity.findall("Tag[@enumID='185']")[0].text
	if nameAttr == name :
		if len(entity.findall("Tag[@enumID='351']")) > 0 :
			#print entity.findall("Tag[@enumID='351']")[0].text
			return entity
	return None

def findOriginalCode(root,name):
	for entity in root.findall(".//Entity") :
		test = findEntity(root,name,entity)
		if test != None :
			descAttr = ''
			comment = ''
			artist = ''
			attack = ''
			health = ''
			cost = ''
			if entity.findall("Tag[@enumID='184']") :
				descAttr = entity.findall("Tag[@enumID='184']")[0].text
			if entity.findall("Tag[@enumID='351']") :
				comment = entity.findall("Tag[@enumID='351']")[0].text
			if entity.findall("Tag[@enumID='342']") :
				artist = entity.findall("Tag[@enumID='342']")[0].text
			if entity.findall("Tag[@enumID='47']") :
				attack = entity.findall("Tag[@enumID='47']")[0].attrib['value']
			if entity.findall("Tag[@enumID='45']") :
				health = entity.findall("Tag[@enumID='45']")[0].attrib['value']
			if len(entity.findall("Tag[@enumID='45']")) == 0 :
				if entity.findall("Tag[@enumID='187']") :
					health = entity.findall("Tag[@enumID='187']")[0].attrib['value']
			if entity.findall("Tag[@enumID='48']") :
				cost = entity.findall("Tag[@enumID='48']")[0].attrib['value']
			return (entity.attrib['CardID'],descAttr,comment,artist,attack,health,cost)

def checkPwn():
    tree = parse("enUS.xml")
    root = tree.getroot()
    checkHearthPwn(root)

def makeLangPack(lang):
	print lang+".xml"
	tree = parse(lang+".xml")
	root = tree.getroot()
	f_json = open('data_ctun.json','r')
	data = json.loads(f_json.read())
	f_json.close()
	for card in data['cards'] :
		name = card['cardName']
		print name
		result = findLangPack(root,card['originalCode'])
		print result
		#print findOriginalCode(root,name)
		card['cardName'] = result[0]
		card['desc'] = removeTag(result[1])
		card['comment'] = removeTag(result[2])
		#card[unicode('확장팩')] = unicode('한여름밤의 카라잔')
		card[unicode('확장팩')] = unicode('고대신의 속삭임')
		card[unicode('세트')] = unicode('-')
	with open(lang+'data.json', 'w') as outfile:
		json.dump(data, outfile, indent=4, sort_keys=True, separators=(',', ':'))

def makeLangPack2(lang):
	tree = parse(lang+".xml")
	root = tree.getroot()
	f_json = open('data_karazan.json','r')
	data = json.loads(f_json.read())
	f_json.close()
	write_data = []
	for card in data['cards'] :
		name = card['cardName']
		print name
		result = findLangPack(root,card['originalCode'])
		print result
		#print findOriginalCode(root,name)
		write_data.append({'id':card['originalCode'],'name':result[0],'description':removeTag(result[1]),'comment':removeTag(result[2])})
		#card[unicode('확장팩')] = unicode('한여름밤의 카라잔')
		
	with open(lang+'data.json', 'w') as outfile:
		json.dump(write_data, outfile, indent=4, sort_keys=True, separators=(',', ':'))

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    new_checkHearthPwn()
    #checkPwn()
    # return
    #lang_pack = ['koKR','deDE','enGB','enUS','esES','esMX','frFR','itIT','jaJP','plPL','ptBR','ruRU','zhCN','zhTW']	
    #lang_pack = ['deDE','enGB','enUS','esES','esMX','frFR','itIT','jaJP','plPL','ptBR','ruRU','zhCN','zhTW']	
    # for lang in lang_pack :
    # 	makeLangPack2(lang)

if __name__ == '__main__':
    main()

