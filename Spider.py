import urllib
import urllib2
import robotparser
import sqlite3
import * from urlparse
import re
import BeautifulSoup from BeautifulSoup

#SQLITE CONNECTION
connection=sqlite3.connect('crawler.sqlite')
cur=connection.cursor()

#CREATE DATABASE IF NOT EXISTS 
cur.executescript('''CREATE TABLE IF NOT EXISTS Pages(
                            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                            url TEXT UNIQUE,
                            html TEXT,
                            error INTETGER,
                            old_page_rank REAL,
                            new_page_rank REAL
                    );
                    CREATE TABLE IF NOT EXISTS Links(
                            source_page_id INTEGER,
                            sink_page_id INTERGER
                    );
                    CREATE TABLE IF NOT EXISTS StartSearch(
                            site TEXT UNIQUE
                    );
                ''')
#URL INPUT FROM WHERE CRAWLING IS TO BE STARTED
start_url=raw_input("ENTER THE URL FROM WHICH CRAWLING IS TO BE STARTED : ")
if(len(start_url)<1) :
    start_url='http://www.dr-chuck.com/'
if(start_url.endswith('/')) :
    start_url=start_url[:-1]
site=start_url
if(start_url.endswith('htm') or start_url.endswith('html')) :
    start_url=start_url[:start_url.rfind('/'))
    site=start_url

#Update the site retrieved from the User Input and Insert or Update it into the Database
if not site :
    cur.execute('''INSERT OR UPDATE INTO StartSearch(site) VALUES(?)''',(site,))
    cur.execute('''INSERT OR UPDATE INTO Pages(url,html,error,old_page_rank,new_page_rank) VALUES(?,?,?,?,?)''',(site,NULL,NULL,1.0,1.0))
    cur.commit()
sites=list()
cur.execute('''SELECT site from StartSearch''')
for row in cur.fetchone() :
    if(row is None) :
        break
    sites.append(str(row))


