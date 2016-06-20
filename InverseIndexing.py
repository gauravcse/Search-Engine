import zlib
import sqlite3
import html2text
import re
from BeautifulSoup import BeautifulSoup


#SQLITE CONNECTION
connection = sqlite3.connect("crawler.sqlite")
cur = connection.cursor()

cur.execute(''' CREATE TABLE IF NOT EXISTS Inverse(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                word TEXT UNIQUE,
                pages TEXT) ''')

#cur.execute('''ALTER TABLE Pages ADD COLUMN indexed INTEGER''')

while True : 
    cur.execute("SELECT id,html FROM Pages WHERE html IS NOT NULL AND indexed is NULL")
    #if len(cur.fetchone()) == 0 :
        #break
    #print cur.fetchone()
    page_id = cur.fetchone()[0]
    html = zlib.decompress(cur.fetchone()[1])
    print page_id
    h = html2text.html2text(html)
    h = h.encode("ascii","ignore")
    h = h.lower()
    h = re.sub('[^A-Za-z0-9]+', ' ', h).split(' ')
    for word in h :
        cur.execute('''INSERT OR IGNORE INTO Inverse(word,pages) VALUES(?,NULL)''',(word,))
        connection.commit()
        cur.execute('''SELECT pages from Inverse WHERE word=?''',(word,))
        pages = cur.fetchone()[0]
        if pages is not None :
            pages = pages + ","+str(page_id)
        else :
            pages = str(page_id)
        cur.execute('''UPDATE Inverse SET pages=? WHERE word=?''',(pages,word))
        cur.execute('''UPDATE Pages SET indexed=? WHERE id=?''',(1,page_id))
        connection.commit()
        print "Done"
connection.commit()
cur.close()
