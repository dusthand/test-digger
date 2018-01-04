# -*- coding: utf-8 -*-
"""
根据京东url地址，获取商品价格
京东请求处理过程，先显示html页面，然后通过ajax get请求获取相应的商品价格
 
1.商品的具体数据在html中的格式，如下(示例)
# product: {
#         skuid: 1310118868,
#         name: '\u9999\u5f71\u77ed\u88d9\u4e24\u4ef6\u5957\u88c5\u5973\u0032\u0030\u0031\u0034\u51ac\u88c5\u65b0\u6b3e\u97e9\u7248\u957f\u8896\u0054\u6064\u4e0a\u8863\u8377\u53f6\u8fb9\u534a\u8eab\u88d9\u6f6e\u0020\u85cf\u9752\u0020\u004d',
#         skuidkey:'7781F505B71CE37A3AFBADA119D3587F',
#         href: 'http://item.jd.com/1310118868.html',
#         src: 'jfs/t385/197/414081450/336886/3070537b/541be890N2995990c.jpg',
#         cat: [1315,1343,1355],
#         brand: 18247,
#         nBrand: 18247,
#         tips: false,
#         type: 2,
#         venderId:38824,
#         shopId:'36786',
#         TJ:'0',
#         specialAttrs:["is7ToReturn-1"],
#         videoPath:'',
#         HM:'0'
#     }
 
2.ajax请求代码如下：
# // 获得数字价格
# var getPriceNum = function(skus, $wrap, perfix, callback) {
#     skus = typeof skus === 'string' ? [skus]: skus;
#     $wrap = $wrap || $('body');
#     perfix = perfix || 'J-p-';
#     $.ajax({
#         url: 'http://p.3.cn/prices/mgets?skuIds=J_' + skus.join(',J_') + '&type=1',
#         dataType: 'jsonp',
#         success: function (r) {
#             if (!r && !r.length) {
#                 return false;
#             }
#             for (var i = 0; i < r.length; i++) {
#                 var sku = r[i].id.replace('J_', '');
#                 var price = parseFloat(r[i].p, 10);
#
#                 if (price > 0) {
#                     $wrap.find('.'+ perfix + sku).html('￥' + r[i].p + '');
#                 } else {
#                     $wrap.find('.'+ perfix + sku).html('暂无报价');
#                 }
#
#                 if ( typeof callback === 'function' ) {
#                     callback(sku, price, r);
#                 }
#             }
#         }
#     });
# };
"""
import urllib
import json
import re
import os
from page_parser import FinallPageParser as PageParser
import httplib,re#发起http请求
import sys,json,datetime,bisect#使用了二分快速查找
from urlparse import urlparse#解析url，分析出url的各部分功能
import socket #设置httplib超时时间
 
 
class JdPrice(object):
    """
    对获取京东商品价格进行简单封装
    """
    def __init__(self, url):
        self.url = url
        self._response = urllib.urlopen(self.url)
        self.html = self._response.read()
 
    def get_product(self):
        """
        获取html中，商品的描述(未对数据进行详细处理，粗略的返回str类型)
        :return:
        """
        product_re = re.compile(r'compatible: true,(.*?)};', re.S)
        product_info = re.findall(product_re, self.html)[0]
        return product_info
 
    def get_product_skuid(self):
        """
        通过获取的商品信息，获取商品的skuid
        :return:
        """
        product_info = self.get_product()
        skuid_re = re.compile(r'skuid: (.*?),')
        skuid = re.findall(skuid_re, product_info)[0]
        return skuid
 
    def get_product_name(self):
        pass
 
    def get_product_price(self):
        """
        根据商品的skuid信息，请求获得商品price
        :return:
        """
        price = None
        skuid = self.get_product_skuid()
        url = 'http://p.3.cn/prices/mgets?skuIds=J_' + skuid + '&type=1'
        price_json = json.load(urllib.urlopen(url))[0]
        if price_json['p']:
            price = price_json['p']
        return price
    def get_info(self):
        parser= PageParser()
        ##htmmparser遇到/>就表示tag结尾，所以必须替换，遇到<br/>替换为BRBR，否则会解析失败
        htmlcontent = self.html
        htmlcontent=re.compile('<br/>').sub('BRBR',htmlcontent)
        parser.feed(htmlcontent)
        finalparseurl=parser.getdata()
        # print finalparseurl
        return finalparseurl

    def download_img(self,path):
        info = self.get_info()
        detail_dir = path+"/detail"
        show_dir = path+"/show"
        if not os.path.exists(detail_dir):
            os.mkdir(detail_dir)
        if not os.path.exists(show_dir):
            os.mkdir(show_dir)
        print "partimgs",info['partimgs']
        print "partimgs_show",info['partimgs_show']
        for imgurl in info['partimgs']:#获取商品介绍的图片
            getimg(show_dir,"http:"+imgurl)
        for imgshowurl in info['partimgs_show']:#获取展示图片
            getimg(detail_dir,"http:"+imgshowurl)

#tool
def remove_dir(dir):
    import os  
    import shutil  
    filelist=[]  
    rootdir=dir
    filelist=os.listdir(rootdir)  
    for f in filelist:  
        filepath = os.path.join( rootdir, f )  
        if os.path.isfile(filepath):  
            os.remove(filepath)  
            print filepath+" removed!"  
        elif os.path.isdir(filepath):  
            shutil.rmtree(filepath,True)  
        print "dir "+filepath+" removed!"

#获取图片的方法
def getimg(imgdir,imgurl):
    print "getimg:",imgdir,imgurl
    imgobj=urlparse(imgurl)
    getimgurl=imgobj.path
    imgtmppathlist=getimgurl.split('/')
    imgname=imgtmppathlist[len(imgtmppathlist)-1]
    if not os.path.exists(imgdir):
        try:
            os.makedirs(imgdir)
        except Exception,e:
            print e
    savefile=imgdir+"/"+imgname
    if not os.path.exists(savefile):
        sendhttp_rult=sendhttp(getimgurl,imgobj.hostname,savefile)
        if sendhttp_rult:
            print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+",sent http request succ,getimg:"+imgurl
        else:
            print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+",sent http request fail,getimg:"+imgurl
    else:
        pass

#定义方法sendhttp，调用httpread，获取结果并替换编码（gbk换为utf-8），并保存到文件中（以免下次再去下载页面，这样就节省了时间）
#
def sendhttp(url,host,savefile):
    #定义http头部，很多网站对于你不携带User-Agent及Referer等情况，是不允许你爬取。
    #具体的http的头部有些啥信息，你可以看chrome，右键审查元素，点击network，点击其中一个链接，查看request header
    headers = {"Host":host,
               "Origin":"http://www.jd.com/",
               "Referer":"http://www.jd.com/",
                "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Accept": "text/html;q=0.9,image/webp,*/*;q=0.8",
               "User-Agent":"Mozilla/3.0 AppleWebKit/537.36 (KHTML,Gecko) Chrome/3.0.w4.",
               "Cookie":"__utmz=qwer2434.1403499.1.1.utmcsr=www.jd.com|utmccn=(refrral)|utmcmd=rferral|utmcct=/order/getnfo.action; _pst=xx89; pin=x9; unick=jaa; cshi3.com=D6045EA24A6FB9; _tp=sdyuew8r9e7r9oxr3245%3D%3D; user-key=1754; cn=0; ipLocation=%u7F0C; ipLoc97; areaId=1; mt_ext2%3a%27d; aview=6770.106|68|5479.665|675.735|6767.100|6757.13730|6ee.9ty711|1649.10440; atw=65.15.325.24353.-4|188.3424.-10|22; __j34|72.2234; __jdc=2343423; __jdve|-; __jdu=3434"
    }
    httprestmp=''
    try:
        httprestmp=httpread(host,url,headers)
        if httprestmp=='':#
            httprestmp=httpread(host,url,headers)
            if  httprestmp=='':#重试2次
                httprestmp=httpread(host,url,headers)
    except Exception,e:
        try:
            httprestmp=httpread(host,url,headers)
            if httprestmp=='':#
                httprestmp=httpread(host,url,headers)
                if  httprestmp=='':#重试2次
                    httprestmp=httpread(host,url,headers)
        except Exception,e:
            print e
        print e
    if  re.search(r'charset=gb2312',httprestmp):#如果是gb2312得编码，就要转码为utf-8（因为全局都使用了utf-8）
        httprestmp.replace("charset=gb2312",'charset=utf-8')
        try:
            httprestmp=httprestmp.decode('gbk').encode('utf-8')#有可能转码失败，所以要加上try
        except Exception,e:#如果html编码本来就是utf8或者转换编码出错的时候，就啥都不做，就用原始内容
            print e
    try:
        with  open(savefile, 'w') as file_object:
            file_object.write(httprestmp)
            file_object.flush()
    except Exception,e:
        print e
    return httprestmp

#定义方法httpread，用于发起http的get请求，返回http的获取内容
#这也是代码抽象的结果，如若不抽象这块代码出来，后续你回发现很多重复的写这块代码
def httpread(host,url,headers):
    httprestmp=''
    try:
        conn = httplib.HTTPConnection(host)
        conn.request('GET',url,None,headers)
        httpres = conn.getresponse()
        httprestmp=httpres.read()
    except Exception,e:
        conn = httplib.HTTPConnection(host)
        conn.request('GET',url,None,headers)
        httpres = conn.getresponse()
        httprestmp=httpres.read()
        print e
    finally:
        if conn:
            conn.close()
    return httprestmp

 
# 测试代码
if __name__ == '__main__':
    
    # url = 'http://item.jd.com/1310118868.html'
    # url = 'http://item.jd.com/1044773.html'
    # jp = JdPrice(url)
    # print jp.get_product_price()
    with open("link.txt","r") as judgefile:
        judgeurl_all_lines=judgefile.readlines()
    print judgeurl_all_lines
    if os.path.exists("price.txt"):
        with open("price.txt",'w') as datafile:
            datafile.close()
    image_dir = "images"
    if os.path.exists(image_dir):
        remove_dir(image_dir)
    else:
        os.mkdir(image_dir)
    index = 0
    for link in judgeurl_all_lines:
        index+=1

        if link.find(".jd.com")>=0:
            cur_dir = image_dir+"/%d"%index
            os.mkdir(cur_dir)
               
            jd = JdPrice(link)
            info =  jd.get_info()
            print unicode(jd.html,"gbk").encode("utf-8")
            title = info["title"]
            with open(cur_dir+"/"+unicode(title,"gbk").encode("utf-8")+".txt",'w') as datafile:
                datafile.writelines(jd.html)
                datafile.close()
            price = jd.get_product_price()
            jd.download_img(cur_dir)
        else:
            price = "?"
        with open("price.txt","a") as datafile:#将爬取完毕好的url写入data.txt
            datafile.writelines(price+"\n")
            # datafile.writelines(unicode(info["title"],"gbk").encode("utf-8")+"\n")



 
 
# htm.decode('gb2312', 'ignore').encode('utf-8')
# f = open('jjs.html', 'w')
# f.write(htm)
# f.close()