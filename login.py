# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 14:54:35 2019

@author: dyou
"""

from bs4 import BeautifulSoup
import requests
import random
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

class Login:

    def __init__(self, session, login_url, captcha_url, username, password):
        self.session = session
        self.username = username
        self.password = password
        self.login_url = login_url
        self.captcha_url = captcha_url
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Host': '1688552.com',
            'Origin': 'http://1688552.com',
            'Referer': 'http://1688552.com/caiYouHuiLoginWeb/app/home?ref=ddd643',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
       }

    def login(self):
        self.get_captcha_image()
        params = {
                'txtLoginCaptcha': self.captcha,
                'txtLoginUsername': self.username,
                'txtLoginPassword': self.password,
                'txtRememberUser': ''
        }
        
        r = self.session.post(self.login_url, json=params, headers=self.headers)
        # print(response.text)
        bs = BeautifulSoup(r.content, 'html.parser')
        print(bs.prettify())
        print('HTTP Status', r.status_code)
        
    def get_captcha_image(self):
        r = self.session.get(self.captcha_url, allow_redirects=True)
        #open('code.jpg', 'wb').write(r.content)
        img_data = Image.open(BytesIO(r.content))
        plt.imshow(img_data)
        plt.show()
        #Image.open('code.jpg').show()
        self.captcha = input('captcha:')
        
def test():
    __login_url__ = 'http://1688552.com/caiYouHuiLoginWeb/app/loginVerification?' + str(random.random() * 10000)
    __captcha_url__ = 'http://1688552.com/caiYouHuiLoginWeb/app/checkCode/image?' + str(random.random() * 100)
    session = requests.Session()
    login = Login(session, __login_url__, __captcha_url__, 'pig', 'pigyear0214')
    login.login()

if __name__ == '__main__':
    test()
