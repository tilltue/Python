# -*- coding:utf-8 -*-

import urllib
from bs4 import BeautifulSoup

def stringReplace(string):
    if string != None:
        return string.replace('"','\'')
    else:
        return ""

def makeInfoParser(f,tds,ths,i):
    f.write(ths[i].string)
    f.write('" : ')
    spans = tds[i].find_all('span')
    if len(spans) > 0 :
        f.write(" [\n\t\t\t\t{\n")
        f.write('\t\t\t\t\t"')
    for j in range(0,2):
        rel_name = spans[j]['rel'] 
        rel_value = spans[j].string
        f.write(stringReplace(rel_name))
        f.write('" : "')
        f.write(stringReplace(rel_value))
        if j != 1 :
            f.write('","')
    f.write('"\n\t\t\t\t} ],\n')

def addTextParser(f,ths,tds,i):
    f.write('comment')
    f.write('" : "')
    #print tds[i].contents[0]
    ival = tds[i].contents[0].contents[0]
    #print ival
    #print len(ival.contents)
    for k in range(0,len(ival.contents)) :
        if ival.contents[k].string != None: 
            f.write(stringReplace(ival.contents[k].string))
    f.write('"\n')

def effectTextParser(f,ths,tds,i):
    f.write(stringReplace(ths[i].string))
    f.write('" : "')
    ival = tds[i].contents[0]
    for k in range(0,len(ival.contents)) :
        #print ival.contents[k].string
        f.write(stringReplace(ival.contents[k].string))
    f.write('",\n')
    
def detailTableParser(f,table):
    ths = table.find_all('th')
    #print 'th num : %d' % len(ths)
    tds = table.find_all('td')
    #print 'td num : %d' % len(tds)
    rel_count = 0
    for i in range(0,len(ths)):
        f.write('\t\t"')
        if ths[i].string == '추가 텍스트':
            addTextParser(f,ths,tds,i)
            continue
        if ths[i].string == '효과':
            effectTextParser(f,ths,tds,i)
            continue
        if ths[i].string != None and tds[i].string != None:
            f.write(stringReplace(ths[i].string))
            #print 'th : ' + ths[i].string
            f.write('" : "')
            f.write(stringReplace(tds[i].string))
            #print 'td : ' + tds[i].string
            f.write('",\n')
        else:
            #print 'makeInfoParser'
            makeInfoParser(f,tds,ths,i)
            rel_count+=2
    return 0

def cardParser_mobile(f,urlString,code):
    
    f.write('\n\t\t"cardCode" : "')
    f.write(stringReplace(code))
    f.write('",')
    
    data = urllib.urlopen(urlString)
    soup = BeautifulSoup(data.read(),from_encoding="euc-kr")
    
    navLine = soup.find_all('body')[0].find('div','navline')
    strong = navLine.find_all('strong')
    cardName = strong[1].string
    cardName = cardName[1:len(cardName)-1]
    print cardName
    f.write('\n\t\t"cardName" : "')
    f.write(stringReplace(cardName))
    f.write('",\n')
    
    cost = soup.find('div','cost')
    cost_val = cost.find('span')
    cost_val = cost_val['class'][0][1:]
    #print cost_val
    f.write('\t\t"cost" : "')
    f.write(stringReplace(cost_val))
    f.write('",\n')
    
    attack = soup.find('div','attack')
    attack_val = attack.find('span')
    attack_val = attack_val['class'][0][1:]
    #print attack_val
    f.write('\t\t"attack" : "')
    f.write(stringReplace(attack_val))
    f.write('",\n')
    
    health = soup.find('div','health')
    health_val = health.find('span')
    health_val = health_val['class'][0][1:]
    #print health_val
    f.write('\t\t"health" : "')
    f.write(stringReplace(health_val))
    f.write('",\n')
    
    table = soup.find('table','cardInfo')
    detailTableParser(f,table)
    return 0

def optionParse(f,lis):
    for li in lis:
        th = li.find('span','th')
        if th != None and th.string == '직업 특화':
            td = li.find('span','td')
            if  td != None:
                percent = td.string[:td.string.find('%')]
                f.write('\n\t\t"직업 특화%" : "')
                f.write(stringReplace(percent))
                f.write('",')
                job = td.string[td.string.find('(직업')+3:td.string.find('/')]
                f.write('\n\t\t"직업" : "')
                f.write(stringReplace(job))
                f.write('",')
                normal = td.string[td.string.find('/공용')+3:td.string.find(')')]
                f.write('\n\t\t"공용" : "')
                f.write(stringReplace(normal))
                f.write('",')
        elif th != None and th.string == '선호 옵션':
            td = li.find('span','td')
            if  td != None:
                f.write('\n\t\t"선호옵션" : [\n\t\t\t{\n\t\t\t\t')
                ops = td.string.split(' / ')
                for op in ops:
                    opString = op[:op.find('(')]
                    f.write('"'+stringReplace(opString))
                    f.write('" :"')
                    valString = op[op.find('(')+1:op.find('%')]
                    f.write(stringReplace(valString))
                    f.write('",')
                f.write('\n\t\t\t}],')
        elif th != None and th.string == '평균 비용':
            td = li.find('span','td')
            if td != None:
                f.write('\n\t\t"평균비용" : "')
                f.write(stringReplace(td.string))
                f.write('",')
    return 0

def deckParser_mobile(f,urlString,code):
    f.write('\n\t\t"deckCode" : "')
    f.write(stringReplace(code))
    f.write('",')
    
    data = urllib.urlopen(urlString)
    soup = BeautifulSoup(data.read(),from_encoding="euc-kr")
    
    article = soup.find_all('body')[0].find('div','article')
    title = article.find('span','title')
    titleString = title.string
    #print title
    if titleString == None: 
        titleString = title.find('span').string
    f.write('\n\t\t"title" : "')
    f.write(stringReplace(titleString))
    f.write('",')
    
    infoClass = soup.find_all('body')[0].find('ul','info')
    #print infoClass
    
    jobClass = infoClass.find('li','name1 text-shadow')
    jobName = jobClass.string[:jobClass.string.find(':')-1]
    #print jobClass.string[:jobClass.string.find(':')-1]
    f.write('\n\t\t"직업제한" : "')
    f.write(stringReplace(jobName))
    f.write('",')
    
    minionClass = infoClass.find('span','minion')
    minionCount = minionClass.string
    #print minionClass.string
    f.write('\n\t\t"하수인" : "')
    f.write(stringReplace(minionCount))
    f.write('",')
    
    abilityClass = infoClass.find('span','ability')
    abilityCount = abilityClass.string
    f.write('\n\t\t"주문" : "')
    f.write(stringReplace(abilityCount))
    f.write('",')
    
    weaponClass = infoClass.find('span','weapon')
    weaponCount = weaponClass.string
    f.write('\n\t\t"무기" : "')
    f.write(stringReplace(weaponCount))
    f.write('",')
    
    lis = infoClass.find_all('li')
    optionParse(f,lis)
    
    cardClass = soup.find_all('body')[0].find('div','deckCardListWrap contentWrap')
    cardCodes = cardClass.find_all('div','card')
    f.write('\n\t\t"카드구성" : [\n\t\t\t{')
    for cardCode in cardCodes:
        f.write('\n\t\t\t\t"'+stringReplace(cardCode['rel'])+'" : "')
        f.write(stringReplace(cardCode.find('span','count').string[1:])+'",')
    f.write('\n\t\t\t}],\n')
    
    ulClass = soup.find_all('body')[0].find('ul','graph-1')
    liClass = ulClass.find_all('li')
    f.write('\n\t\t"비용분포" : [\n\t\t\t{')
    for li in liClass:
        f.write('\n\t\t\t\t"'+stringReplace(li.find('span','th').string)+'" : "')
        #print li
        if li.find('span','text') != None :
            text = li.find('span','text').string
            text = text[text.find('(')+1:text.find('장')]
            f.write(stringReplace(text)+'",')
        else:
            f.write('0",')
    f.write('\n\t\t\t}],\n')
    return 0



def main():
    f = file('deck.txt','w')
    f.write('{\n')
    """
    codes = ['1117','68','257','932','242','299','511','1243','195','654','351','348','311','858','1074','854','584','605','186','404','1659','1401','1019','878','48','1221',
            '1014','1108','985','962','768','140','777','443','1241','397','338','526','365','523','1657','75','1371','336','724','680','287','22','376','1147','430','512','971',
            '268','308','1658','411','457','1091','462','289','994','1073','467',
            '1366','239','1080','1651','767','1141','834','201','1662','648','1686','344','352',
            '859','640','134','715','12','405','513','785','113','614','1158','1099','459','618','976','191','1063','475','700','445','608','1140','1182','205','290',
            '577','395','1369','921','1693','855','211','178','32','596','1023','546','455','629','505','77','86','823','727','132','1109','982',
            '1004','1008','1087','374','189','216','642','997','999','158','466','519','797','1655','886','383','1003','141','1261','766','906','993','296',
            '919','41','496','90','592','149','456','530','896','567','510','891','291','279','36','635','636','969','774','602','601','381','765','753','453',
            '1016','877','555','447','564','476','435','679','594','34','1687','538','763','790','339','304','860','1142','1167','581','421','147',
            '846','481','437','213','742','238','903','582','914','641','192','621','662','587','172','306','1737','424','389','1022','1007','1100','974',
            '363','658','1144','1068','943','609','847','1653','864','1372','23','61','95','69','281','757','67','1174','811','401','556','292','926',
            '37','493','233','285','814','251','391','1135','712','1009','1035','400','904','415','1634','545','254','643','366','754','1092','286',
            '783','950','1373','1026','51','232','818','836','250','1361','1281','1047','1522','1093','1362','773','1189','1133','667','420','28','672','791','748','45','759',
            '830','157','1122','699','890','631','138','756','394','585','960','1064','739','284','1171','810','469','804','825','1050','912','778','755','749','461','1688','1090','315',
            '1084','922','1098','1037','606','940','64','1155','1656','163','70',
            '915','801','1124','180','736','175','525','573','559','436','692','866','282','1029','1650','272','710','1364','531',
            '30','570','622','1365','841','613','1721','145','237','345','220','670','503','1367','1363','1368','9','1370','995','179','887','990','1186',
            '151','630','762','8','734','920','517','979','196','440','708',
            
            #영웅 '893','31','274','930','413','1623'
            ]
    f.write('\t"cards" : [\n')
    """

    codes = ['3244','3243','3241','3236','3232','3231','3230','3228','3077','3076','2739','2737','2734','2714','2712','2710','2709'
             ,'2707','2706','2705','2704','2586','2568','2567','2565','2259','2255','2252','2056','2055','2054','2050','1873','1872'
             ,'1871','1860','1859','1856','1706','1704','1702','1211','1210','1209','1207','1182','1176','1175','1174','1173','1171'
             ,'1170','1167','1164','1163','1160','1159','1158','574'];
    f.write('\t"decks" : [\n')
    for code in codes:
        print code
        f.write('\t{')
        #urlString = 'http://m.inven.co.kr/site/hs/card_detail.php?code=%s' % code
        #cardParser_mobile(f,urlString,code)
        urlString = 'http://m.inven.co.kr/site/hs/deck_detail.php?idx=%s' % code
        deckParser_mobile(f,urlString,code)
        f.write('\t},\n')
    print len(codes)
    f.write('\t]\n}\n')
    f.close()

if __name__ == '__main__':
    main()