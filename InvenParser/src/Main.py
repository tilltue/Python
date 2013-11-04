# -*- coding:utf-8 -*-

import urllib
from bs4 import BeautifulSoup

def detailRightContentParser(f,tables):
    for table in tables:
        ths = table.find_all('th')
        print 'th num : %d' % len(ths)
        tds = table.find_all('td')
        print 'td num : %d' % len(tds)
        n = len(ths)
        for i in range(0,n):
            f.write('"')
            if ths[i].string != None and tds[i].string != None:
                f.write(ths[i].string)
                print 'th : ' + ths[i].string
                f.write('" : ')
                f.write(tds[i].string)
                print 'td : ' + tds[i].string
                f.write('",\n')
                print i
            else:
                print '---'
                f.write(ths[i].string)
                print 'th : ' + ths[i].string
                f.write('" : ')
                print tds[i].contents
                spans = tds[i].find_all('span')
                if len(spans) > 0 :
                    f.write(" [\n {\n")
                for j in range(0,len(spans)):
                    rel_name = spans[j]['rel'] 
                    rel_value = spans[j].string
                    print rel_name
                    print rel_value
                    f.write('"')
                    f.write(rel_name)
                    f.write('" : "')
                    f.write(rel_value)
                    f.write('"')
                    if j != len(spans)-1:
                        f.write(',')
                if len(spans) > 0 :
                    f.write("\n}\n]\n")
                if len(spans) == 0 :
                    f.write('" ')
                    #print len(tds[i].contents)
                    for k in range(0,len(tds[i].contents)):
                        if ths[i].string == '추가 텍스트':
                            i_val = tds[i].contents[k]
                            #print i_val.contents[0].string
                            f.write(i_val.contents[0].string)
                            f.write('"')
                        else:
                            #print tds[i].contents[k]
                            text = tds[i].contents[k].string
                            #print text
                            f.write(text)
                            f.write('",\n')
                
    f.write('\n')
    return 0;

def main():
    print "한글"
    f = file('card.txt','w')
    #start json
    f.write('{')
    data = urllib.urlopen('http://hs.inven.co.kr/dataninfo/card/detail.php?code=1117')
    soup = BeautifulSoup(data.read(),from_encoding="euc-kr")
    div = soup.find_all('div','hsDbCommonTitle')
    cardName = div[0]
    text =  cardName.find('h2')
    print text.string
    f.write('\n"cardName" : "')
    f.write(text.string)
    f.write('",\n')
    div = soup.find_all('div','hsDbCommonDetail')
    cost = div[0].find('div','cost')
    cost_val = cost.find('span')
    cost_val = cost_val['class'][0]
    print cost_val
    f.write('"cost" : "')
    f.write(cost_val)
    f.write('",\n')
    attack = div[0].find('div','attack')
    attack_val = attack.find('span')
    attack_val = attack_val['class'][0]
    print attack_val
    f.write('"attack" : "')
    f.write(attack_val)
    f.write('",\n')
    health = div[0].find('div','health')
    health_val = health.find('span')
    health_val = health_val['class'][0]
    print health_val
    f.write('"health" : "')
    f.write(health_val)
    f.write('",\n')
    right = div[0].find('div','detail-right-content')
    #print right
    tables = right.find_all('table')
    detailRightContentParser(f,tables)

if __name__ == '__main__':
    main()