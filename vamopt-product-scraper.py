import requests
from lxml.html import fromstring
import time
import json
from collections import OrderedDict
import sqlite3
DELAY=1
DBFILE='data.db'
LINKSFILE='links.txt'

with open(LINKSFILE) as f:
    total_links=sum(1 for _ in f)
current_link=1
with open(LINKSFILE,'r') as f, sqlite3.connect(DBFILE) as conn:
	sql = '''create table if not exists PRODUCTS(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    URL TEXT,
    IMAGELINK TEXT,
	DATA BLOB);'''
	conn.execute(sql)
	conn.text_factory=str
	for line in f:
		print "Doing link %5s of %5s... " % (current_link,total_links),
		current_link+=1
		uri=line.strip()
		if uri:
			#keys=[('url',uri)]
			data={}
			r=requests.get(uri)
			if r.status_code!=200:
				print "error %s!" % r.status_code
				continue
			#print r
			doc=fromstring(r.text)
			#print doc.xpath('//div[@id="specifikation"]/table')[0].full_text():
			#data['url']=uri
			image_tag=doc.xpath('//a[@id="example1" and @class="zoom fancybox"]')
			image_link=''
			if image_tag:
				image_link=image_tag[0].get('href')
			if image_link:
				image_link='http://vamopt.ru%s' % image_link
			#keys.append(('image_link',image_link))
			keys=[]
			for element in doc.xpath('//div[@id="specifikation"]/table')[0].getchildren():
				#print element,element.getchildren()[0].text.encode('utf-8'),"<=================>",element.getchildren()[1].text.encode('utf-8')
				#data[element.getchildren()[0].text.strip().encode('utf-8')]=element.getchildren()[1].text.strip().encode('utf-8')
				keys.append((element.getchildren()[0].text.strip().encode('utf-8'),element.getchildren()[1].text.strip().encode('utf-8')))
			data=OrderedDict(keys)
			#print data
			#json.dump(data,outfile,ensure_ascii=False)
			sql = '''INSERT INTO PRODUCTS
        	(URL, IMAGELINK, DATA)
        	VALUES(?, ?, ?);'''
			conn.execute(sql,[uri,image_link,json.dumps(data,ensure_ascii=False)]) 
		print "done."
		time.sleep(DELAY)