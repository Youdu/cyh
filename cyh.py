#!/usr/bin/env python
# coding:utf-8

"""
use Katalon Recorder plugin in Chrome to record operations, and export python
code for reference.
use service in http://www.ruokuai.com/home/pricetype to recognize captcha
images.

"""

import requests
from hashlib import md5
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re
from PIL import Image
import time

ruokuai_username = "pig20190214"
ruokuai_password = "pigyear0214"
ruokuai_soft_id = "122683"
ruokuai_soft_key = "aaa9300a665649d782383bce00174d98"
website = "http://1688552.com"
website_login_url = "http://1688552.com"
website_username = "pig"
website_password = "pigyear0214"
screen_image_file = "screen_image.png"
captcha_image_file = "captcha_image.png"


class RClient(object):

    def __init__(self, username, password, soft_id, soft_key):
        self.username = username
        self.password = md5(password.encode('utf-8')).hexdigest()
        self.soft_id = soft_id
        self.soft_key = soft_key
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        r = requests.post('http://api.ruokuai.com/create.json',
                          data=params, files=files, headers=self.headers)
        print(r.content)
        return r.json()

    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json',
                          data=params, headers=self.headers)
        return r.json()


class CyhWebsite(object):
    def __init__(self, driver, login_url, username, password):
        self.driver = driver
        self.login_url = login_url
        self.username = username
        self.password = password

    def login_with_captcha(self, ruokuai_username, ruokuai_password,
                           soft_id, soft_key):
        """ 使用验证码登陆 """
        # 打开浏览器
        driver = self.driver
        driver.set_window_size(1200, 800)
        driver.get(self.login_url)
        assert "彩友会-公平公正公开！" in driver.title
        # 关闭弹窗
        driver.find_element_by_xpath(
                "(.//*[normalize-space(text()) \
                and normalize-space(.)='X'])[1]/following::img[2]").click()
        time.sleep(2)
        code = ''
        # 获取验证码图片
        # 额外操作以防止在输入验证码时验证码图片刷新
        driver.find_element_by_id("checkLoginCodeImage").click()
        driver.find_element_by_id("txtLoginCode").send_keys('1111')
        driver.find_element_by_id("txtLoginCode").clear()
        driver.find_element_by_id("txtLoginCode").send_keys('')
        time.sleep(2)
        imgsrc = driver.find_element_by_id(
            "checkLoginCodeImage").get_attribute('src')
        if re.match(website_login_url
                    + r'/caiYouHuiLoginWeb/app/checkCode/image*', imgsrc):
            # 页面截屏
            driver.get_screenshot_as_file(screen_image_file)
            # 定位验证码位置和大小
            loc = driver.find_element_by_id("checkLoginCodeImage").location
            size = driver.find_element_by_id("checkLoginCodeImage").size
            left = loc['x']
            top = loc['y']
            right = loc['x'] + size['width']
            bottom = loc['y'] + size['height']
            img = Image.open(screen_image_file).crop(
                    (left, top, right, bottom))
            img.save(captcha_image_file)
            # 识别验证码
            rc = RClient(ruokuai_username, ruokuai_password, soft_id, soft_key)
            code_json = rc.rk_create(
                    open(captcha_image_file, 'rb').read(), 1040)
            print(code_json)
            code = code_json['Result']
            print(code)
            driver.find_element_by_id("txtLoginCode").send_keys(code)
        # 登陆
        driver.find_element_by_id("txtLoginUsername").send_keys(self.username)
        # 额外操作以防止element not interactable的错误
        driver.find_element_by_id("txtLoginPasswordText").click()
        driver.find_element_by_id("txtLoginPassword").send_keys(self.password)
        driver.find_element_by_class_name("btn_log").click()


if __name__ == '__main__':
    chrome_options = Options()
#   chrome_options.add_argument("--headless")       # define headless
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                              options=chrome_options)
    website = CyhWebsite(
            driver, website_login_url, website_username, website_password)
    website.login_with_captcha(ruokuai_username, ruokuai_password,
                               ruokuai_soft_id, ruokuai_soft_key)
