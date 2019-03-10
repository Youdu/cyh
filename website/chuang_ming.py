#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""创名彩票站点的实现

创名彩票站点的入口地址是http://cm909.com
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from .site_base import SiteBase
import time

class ChuangMing(SiteBase):
    """创名彩票站点
    
    """
    
    __url__ = "http://cm557.com"
    __url_record = "http://cm557.com/mobile/new_pc_1/index.html#/gameHome/7"
    __url_xingyunfeiting = "http://cm557.com/mobile/new_pc_1/index.html#/2/85"

    def __init__(self, *args, **kwargs):
        print("ChuangMing初始化")
        try:
            super().__init__(self, *args, **kwargs)
        except Exception as err:
            raise err
    
    def login(self):
        chrome_options = Options()
        #   chrome_options.add_argument("--headless")       # define headless
        self.driver = webdriver.Chrome(
                executable_path=ChromeDriverManager().install(),
                options=chrome_options)
        driver = self.driver
        driver.set_window_size(1920, 1080)
        driver.get(self.__url__)
        
        # 有时候因为自动刷新，需要操作两次
        try:
            self.login_input()
        except StaleElementReferenceException:
            self.login_input()
        
        # 等待用户信息“您好”出现
        try:
            WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="redd"]/div[1]/header/div/ul/li[1]/a'))
                        )
        except TimeoutException:
            print("登录失败")
            return False
        
        return True
        
    def login_input(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        # 输入用户名
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="red"]/div/div[1]/header/div/div/div[1]/input')))
        driver.find_element_by_xpath('//*[@id="red"]/div/div[1]/header/div/div/div[1]/input').click()
        driver.find_element_by_xpath('//*[@id="red"]/div/div[1]/header/div/div/div[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="red"]/div/div[1]/header/div/div/div[1]/input').send_keys(self.username)
        # 输入密码
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="red"]/div/div[1]/header/div/div/div[2]/input')))
        driver.find_element_by_xpath('//*[@id="red"]/div/div[1]/header/div/div/div[2]/input').click()
        driver.find_element_by_xpath('//*[@id="red"]/div/div[1]/header/div/div/div[2]/input').clear()
        driver.find_element_by_xpath('//*[@id="red"]/div/div[1]/header/div/div/div[2]/input').send_keys(self.password)
        # 输入验证码
        captcha = input("输入验证码：")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="red"]/div/div[1]/header/div/div/div[3]/input')))
        driver.find_element_by_xpath('//*[@id="red"]/div/div[1]/header/div/div/div[3]/input').click()
        driver.find_element_by_xpath('//*[@id="red"]/div/div[1]/header/div/div/div[3]/input').clear()
        driver.find_element_by_xpath('//*[@id="red"]/div/div[1]/header/div/div/div[3]/input').send_keys(captcha)
        driver.find_element_by_xpath('//*[@id="red"]/div/div[1]/header/div/div/button[1]').click()
        
    def get_acount_info(self):
        pass
    
    def gamble_xingyunfeiting(self, wager):
        """下注幸运飞艇"""
        
        print("下注幸运飞艇")
        driver = self.driver
        
        # 打开幸运飞艇
        driver.get(self.__url_xingyunfeiting)
        
        # 等待显示有效期数
        season_num_elem = WebDriverWait(driver, 10).until(
                    element_has_valid_season_num((By.XPATH, '//*[@id="85"]/div[2]/div/div[2]/div[1]/div/div[1]/p[2]/span'))
                    )
        season_num_str = season_num_elem.text
        if len(season_num_str) > 0:
            print("幸运飞艇第{}期".format(season_num_str))
        else :
            raise Exception("页面信息加载错误，应显示幸运飞艇第xxxxxxxxxxx期")
        
        # 获取截止投注时间
         # 等待显示有效倒计时，秒数不是0
        season_num_elem = WebDriverWait(driver, 10).until(
                    element_has_valid_count_down((By.XPATH, '//*[@id="85"]/div[2]/div/div[2]/div[1]/div/div[2]/span[5]'))
                    )
        hour_str = driver.find_element_by_xpath('//*[@id="85"]/div[2]/div/div[2]/div[1]/div/div[2]/span[1]').text
        hour = int(hour_str)
        minute_str = driver.find_element_by_xpath('//*[@id="85"]/div[2]/div/div[2]/div[1]/div/div[2]/span[3]').text
        minute = int(minute_str)
        second_str = driver.find_element_by_xpath('//*[@id="85"]/div[2]/div/div[2]/div[1]/div/div[2]/span[5]').text
        second = int(second_str)
        print("距离截止投注时间还有：{}时{}分{}秒".format(hour, minute, second))
        
        if hour == 0 and minute < 1:
            print("距离下注截止时间太短，暂不下注")
            return False
        
        # 下注幸运飞艇->冠军
        self.xingyunfeiting_guanjun(wager[1])
        return True
    
    def xingyunfeiting_guanjun(self, wager):
        print("下注幸运飞艇->冠军")
        wager_dic = {
                    u'[冠军] 1': wager[0],
                    u'[冠军] 2': wager[1],
                    u'[冠军] 3': wager[2],
                    u'[冠军] 4': wager[3],
                    u'[冠军] 5': wager[4],
                    u'[冠军] 6': wager[5],
                    u'[冠军] 7': wager[6],
                    u'[冠军] 8': wager[7],
                    u'[冠军] 9': wager[8],
                    u'[冠军] 10': wager[9],
                    u'[冠军] 大': wager[10],
                    u'[冠军] 小': wager[11],
                    u'[冠军] 单': wager[12],
                    u'[冠军] 双': wager[13],
                    u'[冠军] 龙': wager[14],
                    u'[冠军] 虎': wager[15],
                }
        driver = self.driver
        # 点击幸运飞艇->冠军
        driver.find_element_by_xpath('//*[@id="85"]/div[2]/div/div[3]/div[1]/nav/ul/li[2]').click()
        # 点击冠军1，冠军2，......，大，小，单，双，龙，虎
        for i in range(0, len(wager)):
            if wager[i] > 0:
                xpath = '//*[@id="85"]/div[2]/div/div[3]/div[1]/div[1]/div[2]/ul/li[{}]'.format(i+1)
                driver.find_element_by_xpath(xpath).click()
        
        for i in range(0, len(wager)):
            xpath_key = '//*[@id="85"]/div[2]/div/div[3]/div[1]/div[2]/div[3]/div[1]/ul[{}]/li[1]'.format(i+1)
            xpath_value = '//*[@id="85"]/div[2]/div/div[3]/div[1]/div[2]/div[3]/div[1]/ul[{}]/li[2]/input'.format(i+1)
            try:
                key_elem = driver.find_element_by_xpath(xpath_key)
                value_elem = driver.find_element_by_xpath(xpath_value)
                value_elem.click()
                value_elem.clear()
                value_elem.send_keys(str(wager_dic[key_elem.text]))
            except NoSuchElementException:
                pass
        
        # 点击立即投注
        driver.find_element_by_xpath('//*[@id="85"]/div[2]/div/div[3]/div[1]/div[2]/button').click()

    def wait_xingyunfeiting_result(self):
        """等待幸运飞艇开奖结果"""
        
        print("等待幸运飞艇开奖结果")
        driver = self.driver
        
        # 打开幸运飞艇
        driver.get(self.__url_xingyunfeiting)
        
        # 等待显示有效期数
        season_num_elem = WebDriverWait(driver, 10).until(
                    element_has_valid_season_num((By.XPATH, '//*[@id="85"]/div[2]/div/div[2]/div[1]/div/div[1]/p[2]/span'))
                    )
        season_num_str = season_num_elem.text
        if len(season_num_str) > 0:
            print("幸运飞艇第{}期".format(season_num_str))
        else :
            raise Exception("页面信息加载错误，应显示幸运飞艇第xxxxxxxxxxx期")
        
        # 获取截止投注时间
         # 等待显示有效倒计时，秒数不是0
        season_num_elem = WebDriverWait(driver, 10).until(
                    element_has_valid_count_down((By.XPATH, '//*[@id="85"]/div[2]/div/div[2]/div[1]/div/div[2]/span[5]'))
                    )
        hour_str = driver.find_element_by_xpath('//*[@id="85"]/div[2]/div/div[2]/div[1]/div/div[2]/span[1]').text
        hour = int(hour_str)
        minute_str = driver.find_element_by_xpath('//*[@id="85"]/div[2]/div/div[2]/div[1]/div/div[2]/span[3]').text
        minute = int(minute_str)
        second_str = driver.find_element_by_xpath('//*[@id="85"]/div[2]/div/div[2]/div[1]/div/div[2]/span[5]').text
        second = int(second_str)
        print("距离截止投注时间还有：{}时{}分{}秒".format(hour, minute, second))
        
        first_total_sec = hour * 3600 + minute * 60 + second
        total_sec = first_total_sec
        displayed_time = total_sec
        
        while total_sec != 0 and first_total_sec >= total_sec:
            if total_sec != displayed_time and total_sec % 10 == 0:
                print("距离截止投注时间还有：{}时{}分{}秒".format(hour, minute, second))
                displayed_time = total_sec
            time.sleep(0.5)
            hour_str = driver.find_element_by_xpath('//*[@id="85"]/div[2]/div/div[2]/div[1]/div/div[2]/span[1]').text
            hour = int(hour_str)
            minute_str = driver.find_element_by_xpath('//*[@id="85"]/div[2]/div/div[2]/div[1]/div/div[2]/span[3]').text
            minute = int(minute_str)
            second_str = driver.find_element_by_xpath('//*[@id="85"]/div[2]/div/div[2]/div[1]/div/div[2]/span[5]').text
            second = int(second_str)
            total_sec = hour * 3600 + minute * 60 + second
        
        print("幸运飞艇开奖") 
    
    def gamble_cancel(self):
        print("撤销投注")
        driver = self.driver
        # 点击投注记录，有时候出现点击错误，用打开投注记录页面的方式代替
        #record = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="85"]/div[1]/div[1]/div/ul/li[3]/a')))
        #record.click()
        
        # 打开投注记录页面
        driver.get(self.__url_record)
        wait = WebDriverWait(driver, 10)
        
        # 点击未开奖, 点击一次撤销后，页面刷新，需要重新点击未开奖过滤
        # 暂不处理这个问题，因此只支持首页记录的撤销
        #self.wait_element_stale_and_click('//*[@id="red"]/div/div[2]/div[2]/ul/li[3]/label[2]')
        #time.sleep(1)
        
        # 等待表内容的第一项出现
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="red"]/div/div[2]/div[2]/table/tr[2]/td[1]')))
        elements = driver.find_elements_by_xpath('//*[@id="red"]/div/div[2]/div[2]/table/*')
        print("当前页共显示{}项投注记录".format(len(elements) - 1)) # 减去1，除去表头
        for i in range(0, len(elements)):
            # 撤销链接
            xpath_cancel = '//*[@id="red"]/div/div[2]/div[2]/table/tr[{}]/td[11]/a'.format(i+2)
            try:
                # 等第一项的撤销链接刷新出来
                if i == 0:
                    wait.until(EC.presence_of_element_located((By.XPATH, xpath_cancel)))
                driver.find_element_by_xpath(xpath_cancel)
                self.wait_element_stale_and_click(xpath_cancel)
                confirm = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[3]/button/span')))
                confirm.click()
                print("撤销一项")
            except NoSuchElementException:
                # 当前项没有撤销链接，不需要撤销，继续下一项
                pass
            except TimeoutException:
                pass

class element_has_valid_season_num(object):
    """An expectation for checking that an element has a valid season number.
    
    locator - used to find the element
    returns the WebElement once it has a valid season number
    """
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = driver.find_element(*self.locator)   # Finding the referenced element
        if int(element.text) > 0:
            return element
        else:
            return False

class element_has_valid_count_down(object):
    """An expectation for checking that an element has a valid season number.
    
    locator - used to find the element
    returns the WebElement once it has a valid season number
    """
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = driver.find_element(*self.locator)   # Finding the referenced element
        if int(element.text) > 0:
            return element
        else:
            return False