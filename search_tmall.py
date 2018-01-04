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
import httplib
 
 
class JdPrice(object):
    """
    对获取京东商品价格进行简单封装
    """
    def __init__(self, url):
        self.url = url
        # self._response = urllib.urlopen(self.url)
        # self.html = self._response.read()
        headers = {"Content-type": "application/x-www-form-urlencoded; charset=UTF-8",\
        "Accept": "*/*"}
        params = {'username':'xxxx'}        
        data = urllib.urlencode(params)        
        host = 'www.tmall.com'
        # url = '/login'
        conn = httplib.HTTPSConnection(host)
        print conn.request('POST', url, data, headers)

 
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
 
 
# 测试代码
if __name__ == '__main__':
    url = 'http://detail.tmall.com/item.htm?spm=a221t.7069525.3984727853.205.0mXTw3&id=526890443993&acm=lb-zebra-7942-290546.1003.4.693659&scm=1003.4.lb-zebra-7942-290546.OTHER_526890443993_693659'
    jp = JdPrice(url)
    print jp.html

 
 
# htm.decode('gb2312', 'ignore').encode('utf-8')
# f = open('jjs.html', 'w')
# f.write(htm)
# f.close()