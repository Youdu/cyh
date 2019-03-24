#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""彩友会站点的实现

彩友会站点有多个入口网址，其中包含http://1688552.com等
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException#, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from .site_base import SiteBase
import time

class CaiYouHui(SiteBase):
    """彩友会站点
    
    """

    __url__ = "http://1688552.com"
    __url_xingyunfeiting = "http://1688552.com/caiYouHuiLoginWeb/app/lottery?ref=ddd643"
    __gamble_count = 0
    __window_main_page = None
    __window_game = None
    
    def __init__(self, *args, **kwargs):
        """
        参数：
        --------
        args:
            [0]: url
        """
        
        print("CaiYouHui初始化")
        try:
            SiteBase.__init__(self, *args, **kwargs)
            self.base_url = args[0]
            print("站点地址{}".format(args[0]))
        except Exception as err:
            raise err
    
    def login(self, with_captcha = True):
        chrome_options = Options()
        #   chrome_options.add_argument("--headless")       # define headless
        self.driver = webdriver.Chrome(
                executable_path=ChromeDriverManager().install(),
                options=chrome_options)
        driver = self.driver
        # driver.set_window_size(1920, 1080)
        driver.maximize_window()
        driver.get(self.__url__)
        
        wait = WebDriverWait(driver, 10)
        # 关闭弹窗
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="bottomNavClose"]/img'))).click()
        # 等待关闭弹窗后页面刷新完毕   
        time.sleep(2)
        
        # 有时候因为自动刷新，需要操作两次
        try:
            self.login_input(with_captcha)
        except StaleElementReferenceException:
            self.login_input(with_captcha)
        
        # 等待用户名信息出现
        try:
            wait.until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div[3]/div[2]/div/div[1]/dl/dd[1]/p[1]/a'))
                        )
        except TimeoutException:
            print("登录失败")
            return False
        
        return True
        
    def login_input(self, with_captcha = True):
        driver = self.driver
        wait = WebDriverWait(driver, 5)
        
        # 输入用户名
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="txtLoginUsername"]')))
        element.click()
        element.clear()
        element.send_keys(self.username)
        # 输入密码
        element = wait.until(EC.element_to_be_clickable((By.ID, 'txtLoginPasswordText')))
        element.click()
        element = driver.find_element_by_id("txtLoginPassword")
        element.clear()
        element.send_keys(self.password)
        
        # 输入验证码
#        if with_captcha:
#            # 额外操作以防止在输入验证码时验证码图片刷新
#            element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="checkLoginCodeImage"]')))
#            element.click()
#            element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="txtLoginCode"]')))
#            element.send_keys('1111')
#            element.clear()
#            element.send_keys('')
#            captcha = input("输入验证码：")
#            element.send_keys(captcha)
#
#        driver.find_element_by_class_name("btn_log").click()
        
        # 验证码在窗口切换时会刷新，需要在网页上手动输入，并点击登录
        input("在网页上输入验证码，并点击登录，并关闭弹窗之后，在这里输入回车：")
        
    def get_acount_info(self):
        pass
    
    # 获取开奖信息
    def get_season_info(self, game_name):
        """获取开奖信息"""
        pass
    
    # 下注某一博彩游戏
    # game_name, 博彩游戏名称字符串，如“北京PK10”，“幸运飞艇”等
    def gamble(self, game_name, wager, limit_time_s = 60):
        """下注项目"""
        
        if game_name == "幸运飞艇":
            self.gamble_xingyunfeiting(wager)
        else:
            print("不支持{}".format(game_name))

    def gamble_xingyunfeiting(self, wage):
        """下注幸运飞艇"""
        
        self.__gamble_count = 0
        print("下注幸运飞艇")
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        
        self.__window_main_page = driver.window_handles[0]
        # 打开游戏页面
        element = driver.find_element_by_xpath('//*[@id="li_lottery"]')
        ActionChains(driver).move_to_element(element).perform()
        time.sleep(1)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[3]/div/ul/li[3]/ul/li[4]/a')))
        element.click()
        self.__window_game = driver.window_handles[1]
        driver.switch_to_window(self.__window_game)
        # 下注冠亚组合
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="elem_xyft"]/a[3]')))
        element.click()
        # 冠亚大
        self.input_value('//*[@id="common_div"]/div[2]/table[1]/tbody/tr/td[1]/table/tbody/tr[6]/td[3]/input', 2)
        # 冠亚小
        self.input_value('//*[@id="common_div"]/div[2]/table[1]/tbody/tr/td[2]/table/tbody/tr[6]/td[3]/input', 3)
        
        # 下注三四五六名
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="elem_xyft"]/a[4]')))
        element.click()
        time.sleep(1)
        # 下注七八九十名
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="elem_xyft"]/a[5]')))
        element.click()
        time.sleep(1)
    
    def input_value(self, xpath, value):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
        element.clear()
        element.send_keys(str(value))
        
    def wait_result(self, game_name):
        """等待开奖结果"""
        pass
    
    def gamble_cancel(self):
        """撤销投注"""
        pass
