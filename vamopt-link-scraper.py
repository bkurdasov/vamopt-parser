import requests
from lxml.html import fromstring
import time
DELAY=1
uri='http://www.vamopt.ru/catalog/'
uri='http://www.vamopt.ru/catalog/?ecount=120' #&PAGEN_1=2'
domain='http://www.vamopt.ru'
FILENAME='links.txt'
with open(FILENAME,'w') as f:
	s=requests.Session()
	r=s.get(uri)
	page=fromstring(r.text)
	last_page_number=int(page.xpath('//div[@class="nav-pages"]/a/text()')[-1])
	print last_page_number
	#page.xpath('//div[@class="prodInfo"]/')
	links_to_products=[]
	links_to_products.append(page.xpath('//a[@class="title"]/@href'))
	for link in page.xpath('//a[@class="title"]/@href'):
		f.write(domain+link+'\n')
	for page_number in xrange(2,last_page_number+1):
		print "parsing page {} of {}...".format(page_number,last_page_number)
		#time.sleep(DELAY)
		uri='http://www.vamopt.ru/catalog/?ecount=120&PAGEN_1={}'.format(page_number)
		r=s.get(uri)
		page=fromstring(r.text)
		for link in page.xpath('//a[@class="title"]/@href'):
			f.write(domain+link+'\n')
print "Done!"