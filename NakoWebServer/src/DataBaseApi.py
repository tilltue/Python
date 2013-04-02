'''
Created on 2013. 4. 3.

@author: tilltue
'''

import sqlite3 as lite

con = None
cur = None

def loadDB(name):
	global con
	global cur
	con = lite.connect(name)
	cur = con.cursor()
	cur.execute('SELECT SQLITE_VERSION()');

def insertTable(name):
	cur.execute("insert into book(title) values('title 6')")
	queryString = "SELECT * FROM book"
	cur.execute(queryString)
	cur.close()
	con.commit()
	
	
def numberOfTable(name):
	queryString = "SELECT * FROM %s" % name
	cur.execute(queryString)
	row = cur.fetchall()
	return len(row)

