#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""站点基类的实现

这个模块定义站点基类. 
定义通用的属性：用户名，密码，站点cookies等
定义通用的方法：登陆，获取帐户信息，下注等
"""

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import time

class SiteBase:
    """站点基类
    
    """

    def __init__(self, *args, **kwargs):
        try:
            self.username = kwargs['username']
            self.password = kwargs['password']
            self.speaker = kwargs['speaker']
        except KeyError as err:
            raise Exception("参数缺失{}".format(err))
            
        chrome_options = Options()
        #   chrome_options.add_argument("--headless")       # define headless
        self.driver = webdriver.Chrome(
                executable_path=ChromeDriverManager().install(),
                options=chrome_options)

    def wait_element_stale_and_click(self, xpath):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        elem = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        conitnue_click = True
        while conitnue_click:
            try:
                elem.click()
                conitnue_click = False
            except WebDriverException:
                time.sleep(0.1)
                print("点击页面异常，重试。页面元素XPATH={}".format(xpath))
        return elem
    
    def quit(self):
        driver = self.driver
        driver.close()
    
    def input_value(self, xpath, value):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
        element.clear()
        element.send_keys(str(value))
        