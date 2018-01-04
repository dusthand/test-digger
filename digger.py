#coding=utf-8
import urllib
import json
from string import Template
import thread
import time
import threading  
import re
import requests
import random
import os


threadCount = 0;
countLock =threading.Lock()

def foo(string, encoding = "utf-8"):
	# 1. convert multi-byte string to wide character string
	# 3. convert wide character string to printable multi-byte string
	return string.encode(encoding)


def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def download(url,localPath):
	global threadCount

	changeThreadCount(1)
	#11
	# socket = urllib.urlopen(url)
	# data = socket.read();
	
	# with open(localPath,"wb") as file:
	# 	file.write(data)
	# socket.close()
	#22
	# if localPath.find(".mp4?"):
	# 	i = localPath.find(".mp4?")
	# 	localPath = localPath[0:i+4]
	# elif localPath.find(".m3u8?"):
	# 	i = localPath.find(".m3u8?")
	# 	localPath = localPath[0:i+5]
	try:
		r = requests.get(url)
		randomname = str(int(random.random()*10000000))
		with open(randomname, 'wb') as fd:
			for chunk in r.iter_content():
				fd.write(chunk)
		os.rename(randomname, localPath)
	except Exception,e:
		print "download exception:",e

	changeThreadCount(-1)
	print("finish >>> " +localPath)
	thread.exit_thread()

def changeThreadCount(value):
	global threadCount
	countLock.acquire()
	threadCount+=value
	countLock.release()



def downloadPic( item ,mode):

	name = item["wbody"].encode("utf-8")
	# print "downloadPic:",name
	like = str(int(float(item["likes"].encode("utf-8"))))

	# print(like)
	if mode == 3:
		url = item["vplay_url"].encode("utf-8");
	else:
		url = item["wpic_large"].encode("utf-8")
	print "url"+url
	
	update_time = item["update_time"].encode("utf-8")
	if mode == 4:
		path = "result/girl/"+like+"_"+update_time+"."+url[-3:]
	elif mode == 2:
		path = "result/pic/"+like+"_"+name+"."+url[-3:]
	elif mode == 3:
		suffix = url.split(".")
		suffix = suffix[len(suffix)-1]
		path = "result/video/"+like+"_"+name+"."+suffix

	t = thread.start_new_thread(download, (url,path) )
	# download(url,"Result/pic/"+like+"_"+name+"."+url[-3:])
	# print(url+" "+"result/pic/"+name+"."+url[-3:])


# for item in items:
# 	print item["wbody"].encode("utf-8")




base = 2000.0
baseNum = 2.0;
last_time = -1
urlTextBase = Template( "http://120.55.151.67/weibofun/weibo_list.php?apiver=10500&category=weibo_jokes&page=0&page_size=30&max_timestamp=$update_time&vip=1&platform=iphone&appver=1.6&udid=C0DB3BE4-9CEB-48E5-A278-B7D2D7912343")
urlPicBase = Template("http://120.55.151.67/weibofun/weibo_list.php?apiver=10500&category=weibo_pics&page=0&page_size=30&max_timestamp=$update_time&vip=1&platform=iphone&appver=1.6&udid=C0DB3BE4-9CEB-48E5-A278-B7D2D7912343")
urlGirlBase = Template("http://120.55.151.67/weibofun/weibo_list.php?apiver=10500&category=weibo_girls&page=0&page_size=30&max_timestamp=$update_time&vip=1&platform=iphone&appver=1.6&udid=C0DB3BE4-9CEB-48E5-A278-B7D2D7912343")
urlVideoBase = Template("http://120.55.151.67/weibofun/weibo_list.php?apiver=10500&category=weibo_videos&page=0&page_size=30&max_timestamp=$update_time&vip=1&platform=iphone&appver=1.6&udid=C0DB3BE4-9CEB-48E5-A278-B7D2D7912343")

urls = [];
urls.append(urlTextBase);
urls.append(urlPicBase);
urls.append(urlVideoBase);
urls.append(urlGirlBase);


list  = [];
w = -1
	
type = 2;

statistList = []

for count in xrange(0,100):


	url = urls[type-1].substitute(update_time=last_time)
	print url
	print ".",
	jsonData = getHtml(url)

	data = json.dumps(jsonData,indent = "\t",ensure_ascii=False)
	jdata = json.loads(jsonData)
	items = jdata["items"]



	for item in items:

		like = float(item["likes"])
		update_time = int(item["update_time"])

		# print item["wbody"].encode("utf-8")
		# print like,
		# print baseNum,
		# print base,
		# print baseNum-1,
		# print baseNum

		if baseNum<30 or (like < base*2 and like > base*0.5 ):
			# print base,"get:",like
			base = like/baseNum + base/baseNum*(baseNum-1)
		else:
			pass
			# print base,"    drop:",like


		
		baseNum+=1;
		baseNum = min(30,baseNum)

		
		statistList.append([ like,base ])
		print base
		if base*2.5> like:
			continue

		# print (update_time-54000)%86400

		# if( (update_time-54000)%86400 != 0 ):
		# 	continue;


		while(threadCount >5):
			time.sleep(5)

		downloadPic(item,type)
		list.append(item)
	# for item in items:

	# 	like = float(item["likes"])
	# 	base = like/baseNum + base/baseNum*(baseNum-1)
	# 	baseNum+=1;
	# 	baseNum = min(20,baseNum)


		# wbody = item["wbody"].encode("utf-8")
		# # print  "人是铁" in wbody
		# if  ("人是铁" in wbody) is False:
		# 	continue
		# # else:
		# 	print wbody
		# 	break

	# 	while(threadCount >10):
	# 		time.sleep(5)

		# downloadPic(item,1)
		# list.append(item)

	last_time =  items[len(items)-1]["update_time"]
while(threadCount >0):
	print("rest:"+str(threadCount))
	time.sleep(3)
listData = json.dumps(list,ensure_ascii=False,indent=1)

fout = open("result/weibo_videos.txt","w")
fout.write(listData.encode("utf-8"))
fout.close()

sstr = ""
for m in statistList:
	sstr = sstr+str(m[0])+"\t"+str(m[1])+"\n"
fout = open("result/statist.txt","w")
fout.write(sstr.encode("utf-8"))
fout.close()


# print listData

