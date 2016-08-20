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
	return string

def checkHearthPwn(root):
    #f_json = open('card_eng.txt','r')
    f_json = open('card_eng.txt','r')
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

def findOriginalCode(root,name):
	for entity in root.findall(".//Entity") :
		nameAttr = entity.findall("Tag[@enumID='185']")[0].text
		if nameAttr == name :
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
			if entity.findall("Tag[@enumID='48']") :
				cost = entity.findall("Tag[@enumID='48']")[0].attrib['value']
			
			return (entity.attrib['CardID'],descAttr,comment,artist,attack,health,cost)

def checkPwn():
    tree = parse("enUS.xml")
    root = tree.getroot()
    checkHearthPwn(root)

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    checkPwn()
    lang_pack = ['deDE','enGB','enUS','enES','esMX','frFR','itIT','jaJP','koKR','plPL','ptBR','ruRU']

if __name__ == '__main__':
    main()

