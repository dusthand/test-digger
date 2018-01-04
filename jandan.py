# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import requests
import time
url_base = "http://jandan.net/ooxx/page-%s#comments"

import os
def get_url(url):
	html = requests.get(url)
	# print html.text
	soul = BeautifulSoup(html.text,"lxml")
	links =  soul.select("div .text")
	for link in links:
		# print link
		try:
			link_soul = BeautifulSoup(str(link),"lxml")
			idd =  link_soul.select(".vote")[0].attrs.get("id")[5:]
			up =  int(link_soul.select("#cos_support-%s"%idd)[0].text)
			down =  int(link_soul.select("#cos_unsupport-%s"%idd)[0].text)
			try:
				href = link_soul.select(".view_img_link")[0].attrs.get("href")
			except Exception,e:
				print link
				# print link_soul.select("img")[0]
				href = link_soul.select("img")[0].attrs.get("src")
			if not href:
				print "not href:",link
				continue
			if not href.startswith("http"):
				href = "http:"+href
			postfix = os.path.splitext(href)[-1]
			target_name = "%s%s"%(idd,postfix)
			# print idd,up,down,href,target_name
			# print up,down
			flag = judge_up(up,down)
			if flag:
				try:
					with open('jandan/%s'%target_name, 'wb') as jpg:
						jpg.write(requests.get(href, stream=True).content)
					time.sleep(0.1)
				except Exception,e:
					print "fail download:",href
					print e
		except Exception,e0:
			print e0

		

count = [0,0]
def judge_up(up,down,cache = [20,5]):
	if cache[1] <30:
		cache[0] = (cache[0]*cache[1]+up) /(cache[1]+1)
		cache[1] +=1
	else:
		cache[0] = (cache[0]*29+up) /(30)
	count[1]+=1
	# print up,cache[0],up >cache[0]*2.5,count[0],"/",count[1]
	# print count[0],"/",count[1]
	#2.5--0.176
	#3.5- 0.092
	#4.5 - 0.044
	if up >cache[0]*1.6:
		count[0]+=1
		return True
	else:
		return False


if __name__ == "__main__":
	newest = 2368
	for i in xrange(0,25):
		cur = newest-i
		url = url_base%cur
		print url
		get_url(url)
		time.sleep(1)
