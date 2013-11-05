# -*- coding:utf-8 -*-

import urllib
from bs4 import BeautifulSoup

def detailRightContentParser(f,tables):
    for table in tables:
        ths = table.find_all('th')
        #print 'th num : %d' % len(ths)
        tds = table.find_all('td')
        #print 'td num : %d' % len(tds)
        n = len(ths)
        for i in range(0,n):
            f.write('\t\t"')
            if ths[i].string != None and tds[i].string != None:
                f.write(ths[i].string)
                #print 'th : ' + ths[i].string
                f.write('" : "')
                f.write(tds[i].string)
                #print 'td : ' + tds[i].string
                f.write('",\n')
                #print i
            else:
                #print '---'
                f.write(ths[i].string)
                #print 'th : ' + ths[i].string
                f.write('" : ')
                #print tds[i].contents
                spans = tds[i].find_all('span')
                if len(spans) > 0 :
                    f.write(" [\n\t\t\t\t\t{\n")
                for j in range(0,len(spans)):
                    rel_name = spans[j]['rel'] 
                    rel_value = spans[j].string
                    #print rel_name
                    #print rel_value
                    f.write('\t\t\t\t"')
                    f.write(rel_name)
                    f.write('" : "')
                    f.write(rel_value)
                    f.write('"')
                    if j != len(spans)-1:
                        f.write(',\n')
                if len(spans) > 0 :
                    f.write("\n\t\t\t\t\t}\n\t\t\t\t],\n")
                if len(spans) == 0 :
                    f.write('" ')
                    #print len(tds[i].contents)
                    for k in range(0,len(tds[i].contents)):
                        if ths[i].string == '추가 텍스트':
                            i_val = tds[i].contents[k]
                            #print i_val.contents[0].string
                            f.write(i_val.contents[0].string)
                        else:
                            #print tds[i].contents[k]
                            text = tds[i].contents[k].string
                            print text
                            f.write(text)
                    if ths[i].string == '추가 텍스트':
                        f.write('"\n')
                    else:
                        f.write('",\n')
    return 0

def cardParser(f,urlString):
    data = urllib.urlopen(urlString)
    soup = BeautifulSoup(data.read(),from_encoding="euc-kr")
    div = soup.find_all('div','hsDbCommonTitle')
    cardName = div[0]
    text =  cardName.find('h2')
    print text.string
    f.write('\n\t\t"cardName" : "')
    f.write(text.string)
    f.write('",\n')
    div = soup.find_all('div','hsDbCommonDetail')
    cost = div[0].find('div','cost')
    cost_val = cost.find('span')
    cost_val = cost_val['class'][0]
    #print cost_val
    f.write('\t\t"cost" : "')
    f.write(cost_val)
    f.write('",\n')
    attack = div[0].find('div','attack')
    attack_val = attack.find('span')
    attack_val = attack_val['class'][0]
    #print attack_val
    f.write('\t\t"attack" : "')
    f.write(attack_val)
    f.write('",\n')
    health = div[0].find('div','health')
    health_val = health.find('span')
    health_val = health_val['class'][0]
    #print health_val
    f.write('\t\t"health" : "')
    f.write(health_val)
    f.write('",\n')
    right = div[0].find('div','detail-right-content')
    tables = right.find_all('table')
    detailRightContentParser(f,tables)
    return 0

def main():
    f = file('card3.txt','w')
    f.write('{\n')
    codes = [#'1117','68','257','932','242','299','511','1243','195','654','351','348','311','858','1074','854','584','605','186','404','1659','1401','1019','878','48','1221',
            #'1014','1108','985','962','768','140','777','443','1241','397','338','526','365','523','1657','75','1371','336','724','680','287','22','376','1147','430','512','971',
            #'268','308','1658','411','457','1091','462','289','994','1073','467','1366','1080','1651','767','239','1141','834','201','1662','648','1686','344','352'
            #'915','801','1124','180','440','736','175','525','573'#인코딩 오류
            #영웅 '893'
            ]
    f.write('\t"cards" : [\n')
    for code in codes:
        print code
        f.write('\t\t\t{')
        urlString = 'http://hs.inven.co.kr/dataninfo/card/detail.php?code=%s' % code
        cardParser(f,urlString)
        f.write('\t\t\t},\n')
    f.write('\t]\n}\n')
    f.close()

if __name__ == '__main__':
    main()