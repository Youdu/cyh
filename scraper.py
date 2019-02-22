# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 17:41:11 2019

@author: dyou
"""

from urllib.request import urlopen
# from urllib.request import Request
from bs4 import BeautifulSoup
import re

url = "https://en.wikipedia.org/wiki/Kevin_Bacon"
# =============================================================================
# hdr = {
#        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,\
#            image/webp,image/apng,*/*;q=0.8',
#        'Accept-Encoding': 'gzip, deflate, br',
#        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
#        #'Cache-Control': 'max-age=0',
#        'Connection': 'keep-alive',
#        'Cookie': 'GeoIP=US:OH:Columbus:39.97:-83.02:v4; \
#            WMF-Last-Access=22-Feb-2019; WMF-Last-Access-Global=22-Feb-2019',
#        'Host': 'en.wikipedia.org',
#        #If-Modified-Since: Thu, 21 Feb 2019 07:51:45 GMT
#        #Upgrade-Insecure-Requests: 1
#        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
#        AppleWebKit/537.36 (KHTML, like Gecko) \
#            Chrome/72.0.3626.109 Safari/537.36'
#       }
# req = Request(url, headers=hdr)
# =============================================================================
html = urlopen(url)
bs = BeautifulSoup(html, 'html.parser')
body_content = bs.find('div', {'id': 'bodyContent'})
links = body_content.find_all('a', href=re.compile('^(/wiki/)((?!:).)*$'))
for link in links:
    if 'href' in link.attrs:
        print(link.attrs['href'])
