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

def makeInfoParser(f,tds,ths,i):
    if ths[i].string == None:
        f.write('None');
        f.write(str(i));
        f.write('" : "None",\n');
        return
    else: 
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
    f.write('",\n')

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
    
    imageUrl = soup.find_all('body')[0].find('div','portrait')
    imageUrl = imageUrl['style'] 
    imageUrl = imageUrl[22:imageUrl.find('\');')]
    
    imgF = file('./image/'+code+'.png','w')
    imgContent = urllib.urlopen(imageUrl).read()
    imgF.write(imgContent)
    
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
    for tr in lis:
        th = tr.find('th')
        if th != None and th.string == '직업 특화':
            td = tr.find('td')
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
            td = tr.find('td')
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
            td = tr.find('td')
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
    soup = BeautifulSoup(data.read(),from_encoding="euc-kr")#euc-kr
    
    article = soup.find_all('body')[0].find('div','article')
    title = article.find('span','title')
    titleString = title.string
    print title
    if titleString == None: 
        titleString = title.find('span').string
    f.write('\n\t\t"title" : "')
    f.write(stringReplace(titleString))
    f.write('",')
    
    f.write('\n\t\t"version" : "')
    f.write(stringReplace('2'))
    f.write('",')
    
    articleSpan = article.find('span','article')
    deckDate = articleSpan.string[articleSpan.string.find('갱신일 : ')+6:articleSpan.string.find('갱신일 : ')+11]
    #print deckDate
    f.write('\n\t\t"date" : "')
    if int(code) > 40101 :
        f.write('2015-')
    else :
        f.write('2014-')
    f.write(stringReplace(deckDate))
    #f.write(stringReplace('05-11'))
    f.write('",')
    
    infoClass = soup.find_all('body')[0].find('div','infoContent')
    #print infoClass
    jobClass = infoClass.find('th','name1 text-shadow')
    string = jobClass.contents[0]
    jobName = string[:string.find(':')-1]
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
    
    lis = infoClass.find_all('tr')
    optionParse(f,lis)
    
    cardClass = soup.find_all('body')[0].find('div','deckCardListWrap contentWrap')
    cardCodes = cardClass.find_all('div','card')
    f.write('\n\t\t"카드구성" : [\n\t\t\t{')
    for cardCode in cardCodes:
        check_code = stringReplace(cardCode['rel']);
        check_code = checkNaxxCard(check_code);
        f.write('\n\t\t\t\t"'+check_code+'" : "')
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

def checkHearthPwn(check_code):
    f_json = open('./DB_MATCH.json','r')
    data = json.loads(f_json.read())
    f_json.close()
    #print 'check code'+check_code
    for key, value in data.items():
        if key == check_code:
            #print value
            return value
    return check_code

def checkNaxxCard(check_code):
    naxx_codes = ['nack_29','nack_17','nack_12','nack_14','nack_4','nack_6','nack_3','nack_22','nack_7','nack_26','nack_15','nack_30','nack_21'
                  ,'nack_11','nack_27','nack_25','nack_23','nack_1','nack_8','nack_13','nack_28','nack_24','nack_19','nack_9','nack_5','nack_16'
                  ,'nack_10','nack_2','nack_20','nack_18'
                 ]
    codes = ['1753','1858','1806','1860','1784','1915','1786','1800','1802','1861','1914','1791','1783','1801','1808','1796',
            '1793','1810','1804','1807','1799','1789','1781','1809','1910','1790','1805','1913','1794','1797',
            ]
    for i in range(0,len(codes)) :
        if codes[i] == check_code:
            print str(check_code)
            print naxx_codes[i]
            return naxx_codes[i]
    return check_code

def card():
    f = file('card.txt','w')
    f.write('{\n')
    codes = [#'1117','68','257','932','242','299','511','1243','195','654','351','348','311','858','1074','854','584','605','186','404','1659','1401','1019','878','48','1221',
            #'1014','1108','985','962','768','140','777','443','1241','397','338','526','365','523','1657','75','1371','336','724','680','287','22','376','1147','430','512','971',
            #'268','308','1658','411','457','1091','462','289','994','1073','467','1754',
            #'1366','239','1080','1651','767','1141','834','201','1662','648','1686','344','352',
            #'859','640','134','715','12','405','513','785','113','614','1158','1099','459','618','976','191','1063','475','700','445','608','1140','1182','205','290',
            #'577','395','1369','921','1693','855','211','178','32','596','1023','546','455','629','505','77','86','823','727','132','1109','982',
            #'1004','1008','1087','374','189','216','642','997','999','158','466','519','797','1655','886','383','1003','141','1261','766','906','993','296',
            #'919','41','496','90','592','149','456','530','896','567','510','891','291','279','36','635','636','969','774','602','601','381','765','753','453',
            #'1016','877','555','447','564','476','435','679','594','34','1687','538','763','790','339','304','860','1142','1167','581','421','147',
            #'846','481','437','213','742','238','903','582','914','641','192','621','662','587','172','306','1737','424','389','1022','1007','1100','974',
            #'363','658','1144','1068','943','609','847','1653','864','1372','23','61','95','69','281','757','67','1174','811','401','556','292','926',
            #'37','493','233','285','814','251','391','1135','712','1009','1035','400','904','415','1634','545','254','643','366','754','1092','286',
            #'783','950','1373','1026','51','232','818','836','250','1361','1281','1047','1522','1093','1362','773','1189','1133','667','420','28','672','791','748','45','759',
            #'830','157','1122','699','890','631','138','756','394','585','960','1064','739','284','1171','810','469','804','825','1050','912','778','755','749','461','1688','1090','315',
            #'1084','922','1098','1037','606','940','64','1155','1656','163','70',
            #'915','801','1124','180','736','175','525','573','559','436','692','866','282','1029','1650','272','710','1364','531',
            #'30','570','622','1365','841','613','1721','145','237','345','220','670','503','1367','1363','1368','9','1370','995','179','887','990','1186',
            #'151','630','762','8','734','920','517','979','196','440','708',
            #'1753','1858','1806','1860','1784','1915','1786','1800','1802','1861','1914','1791','1783','1801','1808','1796',
            #'1793','1810','1804','1807','1799','1789','1781','1809','1910','1790','1805','1913','1794','1797',
            #'2035','2085','2017','1992','2016','2024','2004','2075','1939','2012','2233','2093','2063','1988','1934','2074','2172','2054','2057','2040','1937','2249',
            #'2084','2046','1940','2002','2039','2049','2023','2077','2065','1928','1933','2018','2037','2010','2038','2060','2050','2066','2064','2073','2086','2070',
            #'2095','2068','2045','2047','1986','2003','1941','2080','2034','1993','2079','2078','2072','2021','2014','1935','2029','2028','2026','2031','1931','1929',
            #'2069','2087','2052','2025','1938','2001','1998','2048','2011','2225','2082','2055','1985','2053','2094','2044','2096','2009','2051','2056','2022','2033',
            #'2058','1990','2032','2076','2020','2013','2059','2234','1995','2019','2081','1991','2062','1997','1982','2008','2071','1936','2042','2030','2041','2083',
            #'2027','1932','1989','2015','2006','2067','2061','2043','2088','1927','2007','2005','2036'
            '2408','2409','2291','2283','2261','2297','2308','2296','2298','2275','2260','2301','2274','2257','2289','2299','2284','2278','2306','2288','2262',
            '2281','2280','2290','2304','2279','2258','2295','2292','2286','2263'
            #영웅 '893','31','274','930','413','1623'
            ]
    f.write('\t"cards" : [\n')

    for code in codes:
        print code
        f.write('\t{')
        urlString = 'http://m.inven.co.kr/site/hs/card_detail.php?code=%s' % code
        cardParser_mobile(f,urlString,code)
        f.write('\t},\n')
    print len(codes)
    f.write('\t]\n}\n')
    f.close()

def deck():
    f = file('deck.txt','w')
    f.write('{\n')
    codes = [#'4978','4983','4984','4985','4986','5568','5571','5572','5573','6091','6093','6096','6097','6099','6100','6570','6571',
             #'6573','6576','6577','6581','6582','6585','7059','7060','7066','7067','7070','7072','7073','7591','7592','7598','7599',
             #'7600','7601','7602','7603','7604','7994','8020','8021','8022','8023','8025','8026','8027','8028','8853','8854','8855',
             #'8858','8860','8861','8863','8864','8866','8867','8868','8870',
             #'8873','8874','8875','8876','8878','8879','8880','8881','8882','9824','9826','9830','9832','9834','9835','9838','9841',
             #'9842','9844','10764','10765','10769','10770','10771','10774','10775','10776','10779','11642','11643','11645','11646',
             #'11648','11649','12003','12332','12337','12358','12465','12865','12866','12867','12869','12870','12979','12980','12998',
             #'12999','13002','13003','13005','13006','13008','13009',
             #'13522','13524','13525','13526','13529','13530','13532','13533',
             #'13534','13535','13536','14157','14158','14161','14162','14164','14165','14318','14319','14320','14322','14323','14324',
             #'14325','14326','14327',
             #'14328','14329','14330','15038','15039','15042','15043','15045','15046','15051',
             #'15693','15694','15697','15698','15699','15700','15703','15705','16182','16183','16184','16185','16186','16187','16188','16189',
             #'16190','16192'
             #'22446','22447','22448','22449','22451','22452','22453','22456','22457','22458','22459','22460','22461','22462','22463',
             #'22465','22466','22486','22487','22488','22489','22664','22665','22667'
             #'22750','22748','22747','22746','22745','22744'
             #'23275','23276','23277','23278','23280','23288','23289','23290','23291','23292','23293','23431','23433',
             #'23434','23435','23436','23437','23439','23440','23441','23442','23443','23444','23445','23446','23447',
             #'23448','23817','23819','23820','23821','23822','23823','23824','23825','23826','23827','23829','23830',
             #'23833','23834','24180','24181','24183','24184','24185','24188','24189','24190','24192','24194','24195',
             #'24196','24197','24198','24199','24346','24347','24349','24350','24352','24354','24356','24357','24360',
             #'24361','24362','24363','24364','24365','24490','24491','24492','24493','24495','24496','24498','24499',
             #'24500','24501','24502','24503','24504','24506','24507','24508','24510','24512','24513','24514','24841',
             #'24842','24843','24845','24846','24847','24848','24849','24850','24851','24852','24854','24855','24856',
             #'24857','24858','24859','24860','24861','24862','24863','24865','24990','24992','24993','24994','24995',
             #'24996','24997','24998','24999','25000','25011','25012','25013','25016','25017','25018','25019','25020',
             #'25021','25022',
             #'26976','26975','26974','26972','26971','26970','26969','26968','26966','26965','26962','26961','26960',
             #'26959','26958','26955','26953',
             #'27483','27484','27485','27487','27489','27490','27492','27494','27495','27496','27497','27498','27499',
             #'27500','27501','27502','27503','27504','27505','27506'
             #'29970','29969','29968','29967','29966','29965','29964','29963','29962','29961','29959','29958','29956','29955',
             #'29952','29951','29950','29949','29948','29947','29946','29945','29943','29942','29941','29940'
             #,'29939','29938','29937','29936','29935','29934'
             #'31828','31827','31826','31825','31824','31823','31821','31820','31819','31818','31817','31816','31815','31814','31813'
             #,'31812','31811','31810','31809'
             #'32428','32427','32426','32425','32424','32423','32422','32421','32420','32419','32418','32415','32413','32412','32410'
             #,'32409','32408','32407','32406'
             #'33703','33702','33701','33699','33698','33696','33695','33694','33692','33691','33690','33689','33687','33686','33685',
             #'33684','33683','33529','33528','33527','33526','33525','33524','33523','33521','33519','33518','33516','33515','33514',
             #'33513','33512',
             #'34359','34357','34356','34355','34354','34353','34352','34351','34350','34349','34347','34346','34345','34344','34062',
             #'34061','34060','34055','34054','34053','34051','34050','34049','34048','34047','34046','34044','34043','34042','34041',
             #'34040','34038',
             #'36861','36860','36859','36858','36857','36856','36855','36854','36853','36852','36851','36850','36849','36848','36847','36846',
             #'46753','46752','46751','46750','46749','46748','46747','46746','46745','46744','46743','46742','46741','46740','46739','46738',
             #'46737','46736','46735','46734','46733','46732','46731','46730','45130','45129','45128','45127','45126','45125','45124','45123',
             #'45122','45121','45120','45119','45118','45117','45115','45114'
             #'42870','42868','42867','42866','42865','42864','42863','42862','42861','42859','42857','42856','42854','42853','42852','42851',
             #'42561','42560','42559','42558','42557','42556','42555','42554','42553','42552','42550','42549','41899','41898','41897','41896',
             #'41893','41892','41891','41890','41889','41888','41885','41884','40101','40099','40098','40097','40096','40095','39799','39798','39797',
             #'39796','39795','39794','39793','39789','39786','39784','39782','39725','39724','39723','39720','39719','39718','39717','39715',
             #'35719','35718','35717','35716','35715','35714','35713','35712','35711','35710','35709','35708','35707','35706','35704','35703',
             #'34397','34396','34395','34394','34393','34392','34391','34390','34389','34388',
             #'34222','34220','34219','34218','34217','34216',
             #'34214','34213','34212','34211','34209','34208','34207','34206','34205','34203','34202','34200','34199','34198','34197',
             #'34196','34195','34194','34193','34192','34190','34189','34187','34186','34185','34184','34110','34109','34108','34107',
             #'34106','34105','34104','34103','34102',
             #'55383','55382','55381','55378','55376','55374','55373','55372','55370','55369','55368','55367','55366','55364','55363','55362'
             #'56096','56094','56093','56092','56091','56090','56087','56085','56084','56081','56080','56078','56076','56075','56074','56073',
             #'56072','56071','56070','56069','56068','56066','55799','55797','55795','55792','55785','55784','55782','55780','55779','55778',
             #'55777','55775','55772','55770','55769','55768','55767','55766','55764','55762','55761','55759','55758'
             #'57033','57032','57031','57030','57028','57025','57024','57023','57022'
             '71516','71515','71512','71511','71510','71509','71508','71506','71505','71504','71503','71502','71501','71499','71498',
             #'26440','26439','26438','26437','26436','26435','26434','26433','26431','26430','26429','26427','26426',
             #'26287','26286','26285','26284','26283','26282','26281','26279','26278','26277','26276','26274','26273',
             #'26271','26268','26267','26266','26265','26263','25677','25676','25675','25674','25673','25672','25671',
             #'25670','25669','25668','25667','25666','25665','25418','25417','25416','25415','25413','25411','25408',
             #'25407','25406','25401','25400','25398',
             #'17287','17288','17289','17290','17291','17292','17293','17294','17295','17296','17297','17388','17391','17393','17397','17398','17399',
             #'17401','17403','17405','17407','17408','17469','17470','17471','17472','18781','18782','18784','18785','18786','18787','18788','18789',
             #'18790','18791','18792','18881','18882','18884','18885'
             #'19297','19299','19300','19301','19302','19303','19304','19305','19306'
             #'4115','4116','4117','4118','4120','4431','4432','4433','4587','4588','4589','4958','4960','4963','4964','4965','4977',
             #'3819','3821','3888','3889','3890','3891','3892','3893','3894','3895','3896','4107','4110','4111','4112','4113','4114',
             #'3244','3243','3241','3236','3232','3231','3230','3228','3077','3076','2739','2737','2734','2714','2712','2710','2709'
             #,'2707','2706','2705','2704','2586','2568','2567','2565','2259','2255','2252','2056','2055','2054','2050','1873','1872'
             #,'1871','1860','1859','1856','1706','1704','1702','1211','1210','1209','1207','1182','1176','1175','1174','1173','1171'
             #,'1170','1167','1164','1163','1160','1159','1158','574'
             ];
    f.write('\t"decks" : [\n')

    for code in codes:
        print code
        f.write('\t{')
        urlString = 'http://m.inven.co.kr/site/hs/deck_detail.php?idx=%s' % code
        deckParser_mobile(f,urlString,code)
        f.write('\t},\n')
    print len(codes)
    f.write('\t]\n}\n')
    f.close()

def engImageSave(url,code):
    imgF = file('./image/'+code+'.png','w')
    imgContent = urllib.urlopen(url).read()
    imgF.write(imgContent)
    """
    imgG = file('./gold_image/'+code+'_gold.png','w')
    print url[:len(url)-4]+'_gold.png'
    gold = url[:url.rfind('/')]
    preurl = gold[:gold.rfind('/')+1]
    gold = gold[gold.rfind('/')+1:]
    print preurl+str(int(gold)+1)+'/'+code+'_gold.png'
    imgContent = urllib.urlopen(preurl+str(int(gold)+1)+'/'+code+'_gold.png').read()
    imgG.write(imgContent)
    """
    
def passCode(code):
    return 1
    if code == '53' or code == '359' or code == '541' or code == '102' or code == '582' or code == '645' or code == '689' or code == '321' or code == '451' or code == '243' or code == '517':
        return 0
    if code == '231' or code == '403' or code == '662' or code == '669' or code == '287' or code == '200' or code == '318' or code == '9' or code == '358':
        return 0    
    if code == '354' or code == '524' or code == '561' or code == '408' or code == '45' or code == '534' or code == '685' or code == '565' or code == '583':
        return 0
    if code == '121' or code == '116' or code == '204' or code == '430' or code == '133' or code == '111' or code == '334' or code == '58' or code == '485':
        return 0
    if code == '190' or code == '375' or code == '159' or code == '255' or code == '512' or code ==  '21' or code == '469' or code == '653' or code == '195':
        return 0
    if code == '219' or code == '272' or code == '337' or code == '181' or code == '262' or code == '63' or code == '527' or code == '230' or code == '234':
        return 0
    if code == '501' or code == '235' or code == '156' or code == '376' or code == '606' or code == '65' or code == '397' or code == '377' or code == '393':
        return 0
    if code == '599' or code == '622' or code == '455' or code == '115' or code == '381' or code == '387' or  code == '369' or code == '441':
        return 0
    if code == '32' or code == '443' or code == '137' or code == '680' or code == '592':
        return 0
    return 1

def cardEngParser(f,urlString):
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
        cardCode = ''
        h3s = card.find_all('h3')
        for h3 in h3s :
            href = h3.find('a')['href']
            cardCode = href[7:href.find('-')]
            print '"'+cardCode+'":"'+cardCode+'",'
            if passCode(cardCode) == 0 :
                continue
            f.write('\n\t{\n\t\t"cardCode" : "')
            f.write(stringReplace(cardCode))
            f.write('",') 
            cardName = h3.find('a').string
            f.write('\n\t\t"cardName" : "')
            f.write(stringReplace(cardName))
            f.write('",\n')
            #print cardName
        if passCode(cardCode) == 0 :
            continue
        lis = card.find_all('li')
        job_class =''
        faction = ''
        for li in lis :
            #print li.contents[0].string
            if li.contents[0].string == 'Type: ':
                cardType = ''
                if li.contents[1].string == 'Minion':
                    cardType = '하수인'
                elif li.contents[1].string == 'Ability':
                    cardType = '주문'
                elif li.contents[1].string == 'Weapon':
                    cardType = '무기'
                f.write('\t\t"종류" : "')
                f.write(stringReplace(cardType))
                f.write('",\n')
            if li.contents[0].string == 'Class: ':
                #print li.find('a').contents[1].string
                if li.find('a').contents[1].string.find('Paladin') > 0 :
                    job_class = '성기사'
                elif li.find('a').contents[1].string.find('Warlock') > 0 :
                    job_class = '흑마법사'
                elif li.find('a').contents[1].string.find('Shaman') > 0 :
                    job_class = '주술사'
                elif li.find('a').contents[1].string.find('Priest') > 0 :
                    job_class = '사제'
                elif li.find('a').contents[1].string.find('Warrior') > 0 :
                    job_class = '전사'
                elif li.find('a').contents[1].string.find('Mage') > 0 :
                    job_class = '마법사'
                elif li.find('a').contents[1].string.find('Druid') > 0 :
                    job_class = '드루이드'
                elif li.find('a').contents[1].string.find('Hunter') > 0 :
                    job_class = '사냥꾼'
                elif li.find('a').contents[1].string.find('Rogue') > 0 :
                    job_class = '도적'
            if li.contents[0].string == 'Rarity: ':
                rarity = ''
                #print li.find('a').string
                if li.find('a').string == 'Free' :
                    rarity = '무료'
                elif li.find('a').string == 'Common' :
                    rarity = '일반'
                elif li.find('a').string == 'Rare' :
                    rarity = '희귀'
                elif li.find('a').string == 'Epic' :
                    rarity = '영웅'
                elif li.find('a').string == 'Legendary' :
                    rarity = '전설'
                f.write('\t\t"등급" : "')
                f.write(stringReplace(rarity))
                f.write('",\n')
            if li.contents[0].string.find('Crafting') == 0 :
                crafting = li.contents[0].string
                normal = crafting[15:crafting.find(' / ')] 
                golden = crafting[crafting.find(' / ')+3:crafting.find(' (Golden')]
                f.write('\t\t"제작가격" : [\n\t\t\t{\n\t\t\t\t "normal" : "')
                f.write(stringReplace(normal))
                f.write('","golden" : "')
                f.write(stringReplace(golden))
                f.write('"\n\t\t\t} ],\n')
            if li.contents[0].string.find('Arcane Dust Gained') == 0 :
                crafting = li.contents[0].string
                normal = crafting[20:crafting.find(' / ')] 
                golden = crafting[crafting.find(' / ')+3:crafting.find(' (Golden')]
                f.write('\t\t"추출가격" : [\n\t\t\t{\n\t\t\t\t "normal" : "')
                f.write(stringReplace(normal))
                f.write('","golden" : "')
                f.write(stringReplace(golden))
                f.write('"\n\t\t\t} ],\n')
            if li.contents[0].string == 'Faction: ':
                if li.find('span') != None :
                    #print li.find('span').contents[0].string
                    faction = li.find('span').contents[0].string
                    if faction == 'Neutral' :
                        faction = '중립'
                    elif faction == 'Alliance':
                        faction = '얼라이언스'
                    elif faction == 'Horde':
                        faction = '호드'
            if li.contents[0].string.find('Artist: ') == 0 :
                artist = li.contents[0].string[8:] 
                f.write('\t\t"일러스트" : "')
                f.write(stringReplace(artist))
                f.write('",\n')
        #print job_class
        if len(job_class) == 0 : 
            job_class = '공통'
        f.write('\t\t"직업제한" : "')
        f.write(stringReplace(job_class))
        f.write('",\n')
        f.write('\t\t"소속" : "')
        f.write(stringReplace(faction))
        f.write('",\n')
        job_class = ''
        faction = ''    
        cardDesc = ''
        desc = card.find('p')
        if desc != None :
            for i in range(0,len(desc.contents)) :
                if desc.contents[i].string != None :
                    cardDesc += desc.contents[i].string
            #print cardDesc
            f.write('\t\t"효과" : "')
            f.write(stringReplace(cardDesc))
            f.write('",\n')
        comments = card.find('div','card-flavor-listing-text')
        comment_val = ''
        if comments == None:
            comment_val = '-'
        else :
            for comment in comments.contents:
                if comment != '\n':
                    comment_val += comment.string
        #print comment_val
        f.write('\t\t"comment" : "')
        f.write(stringReplace(comment_val))
        
        f.write('",\n\t\t"확장팩" : "')
        #f.write('클래식')
        f.write('한여름밤의 카라잔')
        f.write('"\n\t},')

def baseEngParser(f,urlString,engUrl):
    print urlString
    
    #visual-details-cell
    data = urllib.urlopen(urlString)
    soup = BeautifulSoup(data.read(),from_encoding="en-us")
    trs = soup.find_all('tr')
    data2 = urllib.urlopen(engUrl)
    soup2 = BeautifulSoup(data2.read(),from_encoding="en-us")
    trs2 = soup2.find_all('tr')
    
    engDic = {'0':'0'}
    for tr in trs2:
        td = tr.find_all('td')
        if len(td) == 10:
            card_id = td[0].find('input')['id']
            if card_id != None:
                cardName = td[1].string
                engDic[card_id] = cardName
                           
    #print engDic
    for tr in trs:
        #print tr.contents
        td = tr.find_all('td')
        if len(td) == 10 :
            card_id = td[0].find('input')['id']
            if card_id != None:
                #print card_id
                f.write('\n\t{\n\t\t"cardCode" : "')
                f.write(stringReplace(card_id))
                f.write('",')
                cardName = td[1].string
                f.write('\n\t\t"cardName" : "')
                f.write(stringReplace(cardName))
                f.write('",')
                cardEngName = engDic.get(card_id)
                if cardEngName != None:
                    f.write('\n\t\t"cardNameEng" : "')
                    f.write(stringReplace(cardEngName))
                    f.write('",')
                #print cardName
                cost = td[6].string
                f.write('\n\t\t"마나비용" : "')
                f.write(stringReplace(cost))
                f.write('",')
                attack = td[7].string
                f.write('\n\t\t"공격력" : "')
                if attack==None:
                    f.write('-')
                else:
                    f.write(stringReplace(attack))
                f.write('",')
                health = td[8].string
                f.write('\n\t\t"생명력" : "')
                if health==None:
                    f.write('-')
                else:
                    f.write(stringReplace(health))
                f.write('",')
                desc = td[9].string
                f.write('\n\t\t"효과" : "')
                if desc==None:
                    f.write('-')
                else:
                    f.write(stringReplace(desc))
                f.write('",')
                f.write('\n\t},')
            

def franchParser():
    f = file('card_fr.txt','w')
    f.write('{\n')
    f.write('\t"franch_cards" : [')
    urlString = 'file:///Users/tilltue/Git/Python/InvenParser/src/Hearthstone Card List_fr.html'
    engUrl = 'file:///Users/tilltue/Git/Python/InvenParser/src/Hearthstone Card List.html'
    baseEngParser(f,urlString,engUrl)
    f.write('\t]\n}\n')
    f.close()
    
def hearthdb():
    f = file('card_eng.txt','w')
    f.write('{\n')
    f.write('\t"cards" : [')
    #urlString = 'http://www.hearthpwn.com/cards?display=2&filter-premium=1&filter-set=103&filter-unreleased=1&page=2'
    #크툰
    #urlString = 'http://www.hearthpwn.com/cards?display=2&filter-premium=1&filter-set=105&filter-unreleased=1&page=2'
    #카라잔
    #urlString = 'http://www.hearthpwn.com/cards?display=2&filter-premium=1&filter-set=106&filter-unreleased=1&page=1'
    #클래식
    urlString = 'http://www.hearthpwn.com/cards?display=2&filter-premium=1&filter-set=3&filter-unreleased=1&page=2'
    cardEngParser(f,urlString)
    """
    for i in range(1,3):
        #urlString = 'http://www.hearthpwn.com/cards?page=%d' % i
        urlString = 'http://www.hearthpwn.com/cards?display=2&filter-set=102&filter-unreleased=1&page=%d' % i
        cardEngParser(f,urlString)
    #urlString = 'http://www.hearthpwn.com/cards?filter-set=100'
        #urlString = 'file:///Users/tilltue/Git/Python/InvenParser/src/test.html'
    """
    f.write('\t]\n}\n')
    f.close()
    
def naxx():
    codes = [#'7854','7792','7825','7887','7865','7848','7782','7836','7843',
             #'7806','7857','7798','7762','7781','7800','7805','7814','7813',
             #'7756','7742','7878','7879','7818','7889','7823',
             #'7763',X
             #'7820',
             #'7883','7882','7890','7840','7839','7764','7749','7875','7760',
             #'7871','7873','7855','7801',
             #'7765',X
             '7880','7881','7860','7874',
             '7870','7872','7831','7830','683','7773','7774','7791','7789',
             '7864','7863','7885','7884'             
             ]
    for code in codes:
        urlString = 'http://www.hearthpwn.com/cards/%s' % code
        data = urllib.urlopen(urlString)
        soup = BeautifulSoup(data.read(),from_encoding="en-us")
        card_div = soup.find('div','hearth-tooltip')
        img_url = card_div.find('img')
        print img_url['src']
        engImageSave(img_url['src'],code)

def getJob(job):
    if job.find('Priest') != -1 :
        return '사제'
    elif job.find('Warrior') != -1 :
        return '전사'
    elif job.find('Warlock') != -1 :
        return '흑마법사'
    elif job.find('Rogue') != -1 :
        return '도적'
    elif job.find('Shaman') != -1 :
        return '주술사'
    elif job.find('Mage') != -1 :
        return '마법사'
    elif job.find('Druid') != -1 :
        return '드루이드'
    elif job.find('Hunter') != -1 :
        return '사냥꾼'
    elif job.find('Paladin') != -1 :
        return '성기사'
    
def parseDeck(f,src):
    print src
    data = urllib.urlopen(src)
    soup = BeautifulSoup(data.read(),from_encoding="euc-kr")
    classCards = soup.find_all('body')[0].find('section','t-deck-details-card-list class-listing')
    neutralCards = soup.find_all('body')[0].find('section','t-deck-details-card-list neutral-listing')
    h4 = classCards.find('h4')
    #print classCards
    job =  h4.contents[0].string
    job = getJob(job)
    f.write('\n\t\t"job_class" : "')
    f.write(str(job))
    f.write('",')
    classTbody = classCards.find('table').find('tbody')
    neutralTbody = neutralCards.find('table').find('tbody')
    cards = []
    counts = []
    trs = classTbody.find_all('tr')
    for tr in trs:
        a = tr.find('td').find('a')
        td = tr.find('td','col-name')
        count = '1'
        if td.contents[2].string.find('2') > -1:
            count = '2'
        href = a['href']
        cardCode = href[href.rfind('/')+1:href.find('-')]
        cardCode = checkHearthPwn(cardCode)
        cards.append(cardCode)
        counts.append(count)
    trs = neutralTbody.find_all('tr')
    for tr in trs:
        a = tr.find('td').find('a')
        td = tr.find('td','col-name')
        count = '1'
        if td.contents[2].string.find('2') > -1:
            count = '2'
        href = a['href']
        cardCode = href[href.rfind('/')+1:href.find('-')]
        cardCode = checkHearthPwn(cardCode)
        cards.append(cardCode)
        counts.append(count)
    if len(cards) > 0 :
        f.write('\n\t\t"cards" : [{')
        for i in range(0,len(cards)) :
            f.write('\n\t\t\t"')
            f.write(cards[i])
            f.write('" : "')
            f.write(counts[i])
            f.write('"')
            if i < len(cards)-1:
                f.write(',')    
        f.write('\n\t\t}],')
        
def popularRank():
    f = file('popular.txt','w')
    f.write('{\n')
    f.write('\t"news_id" : "1",\n')
    f.write('\t"type" : "1",\n')
    f.write('\t"title" : "popular deck",\n')
    f.write('\t"title_kor" : "인기 덱 리스트",\n')
    today = date.today();
    f.write('\t"date" : "'+today.isoformat()+'",\n')
    f.write('\t"from" : "HearthPwn",\n')
    f.write('\t"type" : "1",\n')
    f.write('\t"desc" : "",\n')
    f.write('\t"desc_kor" : "",\n')
    f.write('\t"ranks" : [')
    urlString = 'http://www.hearthpwn.com/news/1654-popular-decks-of-the-week-for-august-14'
    data = urllib.urlopen(urlString)
    soup = BeautifulSoup(data.read(),from_encoding="utf-8")
    article = soup.find_all('body')[0].find('tbody','listing-decks')
    trs = article.find_all('tr')
    code = 0
    for i in range(0,len(trs)) :
        tr = trs[i]
        code+=1
        f.write('\n\t{')
        f.write('\n\t\t"rankcode" : "')
        f.write(str(code))
        f.write('",')
        tds = tr.find_all('td')
        for j in  range(0,len(tds)):
            td = tds[j]
            #print td
            a = td.find('a')
            if a != None :
                href = a['href']
                img = td.find('img')
                if img != None:
                    rankName = a.contents[1].string
                    #print a.contents[1].string
                    print rankName
                    f.write('\n\t\t"title" : "')
                    f.write(stringReplace(rankName[1:]))
                    f.write('",')
                if href.find('member') > 0 :
                    member = a.contents[0].string
                    print member
                    f.write('\n\t\t"author" : "')
                    f.write(stringReplace(member))
                    f.write('",')
            strong = td.find('strong')
            print strong
            if strong != None:
                dust = strong.string
                f.write('\n\t\t"dust" : "')
                f.write(stringReplace(dust))
                f.write('"')
            if href.find('decks') > -1 :
                parseDeck(f,href)
        if i < len(trs)-1 :
            f.write('\n\t},')
        else:
            f.write('\n\t}')
    #print trs
    f.write(']\n}\n')
    f.close()
        
def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #card()
    #deck()
    hearthdb()
    #franchParser()
    #popularRank()
        
if __name__ == '__main__':
    main()