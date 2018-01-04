 # -*- coding: utf-8 -*-
 
from HTMLParser import HTMLParser#用于解析html的库，有坑：如果2.6的python，可能悲剧
import re

#定义一个FinallPageParser，用于解析最终的html页面，如http://item.jd.com/1258277.html
#FinallPageParser的定义过程参考上个parser，关键是怎样分析页面，最终写出代码，并且验证，这里就不详细说了
class FinallPageParser(HTMLParser):
    def __init__(self):
        self.handledtags=['div','h1','strong','a','del','div','img','li','span','tbody','tr','th','td','i']
        self.processing=None
        self.title=''
        self.jdprice=''
        self.refprice=''
        self.partimgs_show=set()#展示图片
        self.partimgs=set()#详情图片
        self.partdetail={}#商品详情，参数等
        self.specification=[]#规格参数
        self.typeOrsize=set()#尺码和类型
        self.div=''
        self.flag={}
        self.flag['refprice']=''
        self.flag['title']=''
        self.flag['jdprice']=''
        self.flag['typeOrsize']=''
        self.flag['partimgs']=''
        self.flag['partdetail']=''
        self.flag['specification']=''
        self.flag['typeOrsize']=''
        self.link=''
        self.partslinks={}
        HTMLParser.__init__(self)
    def handle_starttag(self, tag, attrs):
        self.titleflag=''
        self.flag['refprice']=''
        self.flag['title']=''
        self.flag['jdprice']=''
        self.flag['typeOrsize']=''
        self.flag['partimgs']=''
        self.flag['partdetail']=''
        self.flag['specification']=''
        self.flag['typeOrsize']=''
        if tag in self.handledtags:
            self.data=''
            self.processing=tag
            if tag=='div':
                for key,value in attrs:
                    self.div=value# 取出div的name，判断是否是所需要的图片等元素
            if tag=='i':
                self.flag['typeOrsize']='match'
            if tag=='a' and len(attrs)==2:
                tmpflag=""
                for key,value in attrs:
                    if key=='href' and re.search(r'^http:\/\/item.jd.com\/[0-9]{1,10}.html$',value):
                        tmpflag="first"
                    if key=='title' and value!="":
                        tmpflag=tmpflag+"second"
                if tmpflag== "firstsecond":
                    self.flag['typeOrsize']='match'
            if tag=='h1':
                self.flag['title']='match'
            if tag=='strong' and len(attrs)==2:
                for tmpclass,id in attrs:
                    if id=='jd-price':
                        self.flag['jdprice']='match'
            if tag=='del':
                self.flag['refprice']='match'
            if tag=='li':
                self.flag['partdetail']='match'
            if tag=='th' or tag=='tr' or tag=='td' :#++++++++############################################879498.html td中有br的只取到第一个,需要把<br/>喜欢为“”
                self.flag['specification']='match'
            if tag=='img' :
                imgtmp_flag=''
                imgtmp=''
                for key,value in attrs:
                    # print key,value
                    if re.search(r'^//img.*jpg|^//img.*gif|^//img.*png',str(value)) and (key=='src' or key=='data-lazyload'):
                        imgtmp=value
                    if key== 'width':############可能还有logo
                        if re.search(r'^\d{1,9}$',value):
                            if int(value)<=160:
                                imgtmp_flag='no'
                                break
                if self.div=="spec-items" and imgtmp!='':
                    imgtmp=re.compile("/n5/").sub("/n1/",imgtmp)
                    self.partimgs_show.add(imgtmp)
                elif imgtmp_flag!='no' and imgtmp!='':
                    self.partimgs.add(imgtmp)#
    def handle_data(self, data):
        if self.processing:
            self.data+=data
            if self.flag['title']=='match':#获取成功
                self.title=data
            if self.flag['jdprice']=='match':
                self.jdprice=data.strip()
            if self.flag['typeOrsize']=='match':
                self.typeOrsize.add(data.strip())
            if self.flag['refprice']=='match':
                self.refprice=data.strip()
            if self.flag['partdetail']=='match' and re.search(r'：',data):#获取成功
                keytmp=data.split("：")[0].strip()
                valuetmp=data.split("：")[1].strip()
                self.partdetail[keytmp]=valuetmp
            if self.flag['specification']=='match' and data.strip() != '' and data.strip()!='主体':
                self.specification.append(data.strip())
        else:
            pass
    def handle_endtag(self, tag):
        if tag==self.processing:
            self.processing=None
    def getdata(self):
        return {'title':self.title,'partimgs_show':self.partimgs_show,'jdprice':self.jdprice,'refprice':self.refprice,'partimgs':self.partimgs,'partdetail':self.partdetail,'specification':self.specification,'typeOrsize':self.typeOrsize}
