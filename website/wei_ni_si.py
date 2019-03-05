#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""威尼斯彩乐园站点的实现

威尼斯彩乐园站点的入口地址是http://138nan.com
"""

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .site_base import SiteBase
import time

class WeiNiSi(SiteBase):
    """威尼斯彩乐园站点
    
    """
    
    __url__ = "http://138nan.com"

    def __init__(self, *args, **kwargs):
        print("WeiNiSi初始化")
        try:
            super().__init__(self, *args, **kwargs)
        except Exception as err:
            print("{}。将以游客身份登陆".format(err))
            self.login_as_visitor = True
    
    def login(self):
        if self.login_as_visitor:
            chrome_options = Options()
            #   chrome_options.add_argument("--headless")       # define headless
            self.driver = webdriver.Chrome(
                    executable_path=ChromeDriverManager().install(),
                    options=chrome_options)
            driver = self.driver
            driver.set_window_size(1200, 800)
            driver.get(self.__url__)
            driver.find_element_by_id("guestLogin").click()
            driver.find_element_by_id("notClose1").click()
        
    def get_acount_info(self):
        pass
    
    def gamble(self):
        """下注"""
        
        driver = self.driver
        openstime = driver.find_element_by_id("openstime").text
        resultstime = driver.find_element_by_id("resultstime").text
        print("距离封盘：{} 距离开奖：{}".format(openstime, resultstime))
        # 时间格式mm:ss
        if openstime[0:2] == '00' and int(openstime[3:-1]) <= 5:
            print("距离封盘时间太短，不能下注")
            return
        driver.find_element_by_id("cash_37565").clear()
        driver.find_element_by_id("cash_37565").send_keys("1")
        driver.find_element_by_id("send_btn2").click()
        try:
            element = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.LINK_TEXT, u"下注"))
                    )
        finally:
            pass
        element.click()
    
    def gamble_jisusaiche_a(self):
        """下注极速赛车A"""
        
        driver = self.driver
        openstime = driver.find_element_by_id("lot_pk8").click()
        WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "cashval2"))
                    )
        openstime = driver.find_element_by_id("openstime").text
        resultstime = driver.find_element_by_id("resultstime").text
        print("距离封盘：{} 距离开奖：{}".format(openstime, resultstime))
        # 时间格式mm:ss
        if openstime[0:2] == '00' and int(openstime[3:]) <= 5:
            print("距离封盘时间太短，不能下注")
            return
        driver.find_element_by_id("cash_60898").clear()
        driver.find_element_by_id("cash_60898").send_keys("1")
        driver.find_element_by_id("send_btn2").click()
        try:
            element = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.LINK_TEXT, u"下注"))
                    )
        finally:
            pass
        element.click()

    def wait_result(self):
        """等待开奖结果"""
        
        driver = self.driver
        openstime = driver.find_element_by_id("openstime").text
        resultstime = driver.find_element_by_id("resultstime").text
        print("距离封盘：{} 距离开奖：{}".format(openstime, resultstime))
        while True:
            if int(openstime[0:2]) == 0 and int(openstime[3:] == 0):
                break
            else:
                time.sleep(1)
                openstime = driver.find_element_by_id("openstime").text
                resultstime = driver.find_element_by_id("resultstime").text
                print("距离封盘：{} 距离开奖：{}".format(openstime, resultstime))        
