'''AUTHOR : GAURAV MITRA    '''
'''CRAWLER FOR ADDING WEB PAGES TO DATABASE    '''


import urllib
import urllib2
import robotparser
import sqlite3
import urlparse
import re
import zlib
from BeautifulSoup import BeautifulSoup

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
    start_url=start_url[:start_url.rfind('/')]
    site=start_url

#Update the site retrieved from the User Input and Insert or Update it into the Database
if site :
    #print site
    cur.execute('''INSERT OR IGNORE INTO StartSearch(site) VALUES(?)''',(site,))
    cur.execute('''INSERT OR IGNORE INTO Pages(url,html,error,old_page_rank,new_page_rank) VALUES(?,NULL,NULL,?,?)''',(site,1.0,1.0))
    connection.commit()
sites=list()
cur.execute('''SELECT site from StartSearch''')
#print cur.fetchone()[0]
if cur.fetchone()[0] is not None :
    for row in cur.fetchone()[0] :
        if(row is None) :
            break
        sites.append(row)
count=0
while True :
    decision=raw_input("Do You Want to Read another Page ? :")
    if(decision.lower() is "no") :
        #print decision.lower()
        continue
    else :
        cur.execute('''SELECT url from Pages WHERE html IS NULL and error IS NULL''')
        
        webpage=cur.fetchone()[0]
        parsed_url=urlparse.urlparse(webpage)
        main_webpage=str(parsed_url.scheme)+"://"+str(parsed_url.netloc)+"/robots.txt"
        robot=robotparser.RobotFileParser()
        robot.set_url(main_webpage)
        robot.read()
        if(robot.can_fetch("*",webpage) is True) :
            try :
                fetched_page=urllib.urlopen(webpage)
                html_page=fetched_page.read()
                if fetched_page.getcode()!=200 :
                    print '{0} : {1}'.format("Error Retrieving Page.    ERROR NUMBER",fetched_page.getcode())
                    cur.execute('''UPDATE Pages SET error=? WHERE url=?''',(fetched_page.getcode(),webpage))
                    connection.commit()
                    continue
                if fetched_page.info().gettype() != 'text/html' :
                    print '{0}'.format("NOT PARSABLE PAGE")
                    cur.execute('''DELETE FROM Pages where url=?''',(webpage,))
                    connection.commit()
                    continue
                print '{0} : {1}'.format("Website visited",webpage)
                print '{0}  {1}'.format("Length of The Page(in characters) : ",len(html_page))
                soup=BeautifulSoup(html_page)
                cur.execute('''UPDATE Pages SET error=?,html=? WHERE url=?''',(200,buffer(zlib.compress(html_page)),webpage))
                connection.commit()
            except KeyboardInterrupt:
                print '{}'.format("PROGRAM INTERRUPTED BY USER")
                break
            
                
            #CONTINUE FROM SOUP = BS(HTML_PAGE)
            tags=soup('a')
            to_id=list()
            cur.execute('''SELECT id FROM Pages WHERE url=?''',(webpage,))
            from_id=int(cur.fetchone()[0])
            for tag in tags :
                link=tag.get('href',None)
                if link is None :
                    continue
                href=urlparse.urlparse(link)
                if (len(href.scheme)<1 ) :
                    href=urlparse.urljoin(webpage,href)
                pos = link.find('#')
                if ( pos > 1 ) :
                    link = link[:pos]
                if ( link.endswith('.png') or link.endswith('.jpg') or link.endswith('.gif') ) :
                    continue
                if ( link.endswith('/') ) :
                    link = link[:-1]
                if len(link) < 1:
                    continue
#TO CHECK WHETHER THIS IS PRESENT IN ANY OF THE WEBS
                found = False
                for site in sites:
                    if ( link.startswith(site) ) :
                        found = True
                        break
                    if not found :
                        continue

                cur.execute('''INSERT OR IGNORE INTO StartSearch(site) VALUES(?)''',(link,))
                cur.execute('''INSERT OR IGNORE INTO Pages(url,html,old_page_rank,new_page_rank) VALUES(?,NULL,?,?)''',(link,1.0,1.0))
                connection.commit()
                cur.execute('''SELECT id FROM Pages WHERE url=?''',(link,))
                to_id.append(int(cur.fetchone()[0]))
            for pid in to_id :
                cur.execute('''INSERT INTO Links(source_page_id,sink_page_id) VALUES(?,?)''',(from_id,pid))
            connection.commit()
cur.close()
#WHEN ROBOT CANNOT FETCH THE WEBPAGE(Unethical)
'''else : cur.execute(UPDATE'''
            
                
            
            

        
        
