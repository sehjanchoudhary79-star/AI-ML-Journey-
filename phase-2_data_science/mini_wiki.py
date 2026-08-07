import sqlite3
import urllib.request
from bs4 import BeautifulSoup

file=sqlite3.connect('knowledge.sqlite')
cur=file.cursor()

cur.execute(''' CREATE TABLE IF NOT EXISTS Topics(
            ID  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            topic TEXT UNIQUE,
            summary TEXT ,
            url TEXT )''')

file.commit()

def scrape_topic(topic):
    url ="https://en.wikipedia.org/wiki/"+topic.replace(" ","_")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html,'html.parser')

    paragraphs=soup.find_all('p')
    for p in paragraphs:
        if len(p.text.strip())>100:
            return p.text.strip(),url
    return "No Summary Found",url

def save_topic(topic,summary,url):
    cur.execute(''' INSERT OR IGNORE INTO TOPICS (topic,summary,url) VALUES(?,?,?)''',
                 (topic,summary,url))   
    file.commit()
    print("Saved",topic) 

def search_topics(keyword):
    cur.execute('''SELECT topic,summary FROM TOPICS WHERE Topic LIKE?''',
      ('%'+keyword+'%',) )  
    rows=cur.fetchall() 
    for row in rows:
        print('topic',row[0])
        print('summary',row[1])
        print('___')

while True:
    print('\n1.search topic')
    print('2.search saved topics')
    print('3.quit')

    choice=input('choose:')    

    if choice=='1':
        topic=input('enter the topic:')
        summary,url=scrape_topic(topic)
        save_topic(topic,summary,url)
        print('Summary',summary[:300])

    elif choice=='2':
        keyword=input('enter the keyword:')
        search_topics(keyword)

    elif choice=='3':
        break        


    


