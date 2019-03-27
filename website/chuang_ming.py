#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""创名彩票站点的实现

创名彩票站点的入口地址是http://cm909.com
"""

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
    __url_item = "http://cm557.com/mobile/new_pc_1/index.html#/2/{}"
    __gamble_count = 0

    def __init__(self, *args, **kwargs):
        print("ChuangMing初始化")
        try:
            super().__init__(self, *args, **kwargs)
        except Exception as err:
            raise err
    
    def login(self, with_captcha = True):
        driver = self.driver
        # driver.set_window_size(1920, 1080)
        driver.maximize_window()
        driver.get(self.__url__)
        
        # 有时候因为自动刷新，需要操作两次
        try:
            self.login_input(with_captcha)
        except StaleElementReferenceException:
            self.login_input(with_captcha)
        
        # 等待用户信息“您好”出现
        try:
            WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="redd"]/div[1]/header/div/ul/li[1]/a'))
                        )
        except TimeoutException:
            print("登录失败")
            return False
        
        return True
        
    def login_input(self, with_captcha = True):
        driver = self.driver
        # 输入用户名
        self.wait_element_stale_and_click('//*[@id="red"]/div/div[1]/header/div/div/div[1]/input')
        driver.find_element_by_xpath('//*[@id="red"]/div/div[1]/header/div/div/div[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="red"]/div/div[1]/header/div/div/div[1]/input').send_keys(self.username)
        # 输入密码
        self.wait_element_stale_and_click('//*[@id="red"]/div/div[1]/header/div/div/div[2]/input')
        driver.find_element_by_xpath('//*[@id="red"]/div/div[1]/header/div/div/div[2]/input').clear()
        driver.find_element_by_xpath('//*[@id="red"]/div/div[1]/header/div/div/div[2]/input').send_keys(self.password)
        # 输入验证码
        if with_captcha:
            captcha = input("输入验证码：")
            self.wait_element_stale_and_click('//*[@id="red"]/div/div[1]/header/div/div/div[3]/input')
            driver.find_element_by_xpath('//*[@id="red"]/div/div[1]/header/div/div/div[3]/input').clear()
            driver.find_element_by_xpath('//*[@id="red"]/div/div[1]/header/div/div/div[3]/input').send_keys(captcha)

        self.wait_element_stale_and_click('//*[@id="red"]/div/div[1]/header/div/div/button[1]')
        
        
    def get_acount_info(self):
        pass
    
    # 项目的XPATH定位表
    id_table = {
            '北京PK10': 68,
            '幸运飞艇': 85}
    name_table = {
            #0: '冠、亚军和',
            1: '冠军',
            2: '亚军',
            3: '第三名',
            4: '第四名',
            5: '第五名',
            6: '第六名',
            7: '第七名',
            8: '第八名',
            9: '第九名',
            10: '第十名'}
    
    def get_item_key_index(self, item_num):
        name = self.name_table[item_num]
        if item_num >= 1:
            key_index = {
                    0: '[{}] 1'.format(name),
                    1: '[{}] 2'.format(name),
                    2: '[{}] 3'.format(name),
                    3: '[{}] 4'.format(name),
                    4: '[{}] 5'.format(name),
                    5: '[{}] 6'.format(name),
                    6: '[{}] 7'.format(name),
                    7: '[{}] 8'.format(name),
                    8: '[{}] 9'.format(name),
                    9: '[{}] 10'.format(name),
                    10: '[{}] 大'.format(name),
                    11: '[{}] 小'.format(name),
                    12: '[{}] 单'.format(name),
                    13: '[{}] 双'.format(name),
                    14: '[{}] 龙'.format(name),
                    15: '[{}] 虎'.format(name),
                }
        else: # 冠、亚军和
            key_index = {
                    0: '[{}] 冠亚大'.format(name),
                    1: '[{}] 冠亚小'.format(name),
                    2: '[{}] 冠亚单'.format(name),
                    3: '[{}] 冠亚双'.format(name),
                    4: '[{}] 3'.format(name),
                    5: '[{}] 4'.format(name),
                    6: '[{}] 5'.format(name),
                    7: '[{}] 6'.format(name),
                    8: '[{}] 7'.format(name),
                    9: '[{}] 8'.format(name),
                    10: '[{}] 9'.format(name),
                    11: '[{}] 10'.format(name),
                    12: '[{}] 11'.format(name),
                    13: '[{}] 12'.format(name),
                    14: '[{}] 13'.format(name),
                    15: '[{}] 14'.format(name),
                    16: '[{}] 15'.format(name),
                    17: '[{}] 16'.format(name),
                    18: '[{}] 17'.format(name),
                    19: '[{}] 18'.format(name),
                    20: '[{}] 19'.format(name),
                }
        
        return key_index        
    
    # 组装和下注项目对应的下注金额
    def get_sub_wager(self, item_num, wager):
        name = self.name_table[item_num]
        wager_dic = {}
        if item_num >= 1:
            if wager[name]:
                wager_dic = {
                        '[{}] 1'.format(name): wager[name][1] if 1 in wager[name] else 0,
                        '[{}] 2'.format(name): wager[name][2] if 2 in wager[name] else 0,
                        '[{}] 3'.format(name): wager[name][3] if 3 in wager[name] else 0,
                        '[{}] 4'.format(name): wager[name][4] if 4 in wager[name] else 0,
                        '[{}] 5'.format(name): wager[name][5] if 5 in wager[name] else 0,
                        '[{}] 6'.format(name): wager[name][6] if 6 in wager[name] else 0,
                        '[{}] 7'.format(name): wager[name][7] if 7 in wager[name] else 0,
                        '[{}] 8'.format(name): wager[name][8] if 8 in wager[name] else 0,
                        '[{}] 9'.format(name): wager[name][9] if 9 in wager[name] else 0,
                        '[{}] 10'.format(name): wager[name][10] if 10 in wager[name] else 0,
                        '[{}] 大'.format(name): wager[name]['大'] if '大' in wager[name] else 0,
                        '[{}] 小'.format(name): wager[name]['小'] if '小' in wager[name] else 0,
                        '[{}] 单'.format(name): wager[name]['单'] if '单' in wager[name] else 0,
                        '[{}] 双'.format(name): wager[name]['双'] if '双' in wager[name] else 0,
                        '[{}] 龙'.format(name): wager[name]['龙'] if '龙' in wager[name] else 0,
                        '[{}] 虎'.format(name): wager[name]['虎'] if '虎' in wager[name] else 0,
                    }
        else: # 冠、亚军和
            if wager['冠亚军和']:
                wager_dic = {
                        '[{}] 冠亚大'.format(name): wager['冠亚军和']['冠亚大'] if '冠亚大' in wager['冠亚军和'] else 0,
                        '[{}] 冠亚小'.format(name): wager['冠亚军和']['冠亚小'] if '冠亚小' in wager['冠亚军和'] else 0,
                        '[{}] 冠亚单'.format(name): wager['冠亚军和']['冠亚单'] if '冠亚单' in wager['冠亚军和'] else 0,
                        '[{}] 冠亚双'.format(name): wager['冠亚军和']['冠亚双'] if '冠亚双' in wager['冠亚军和'] else 0,
                        '[{}] 3'.format(name): wager['冠亚军和'][3] if 3 in wager['冠亚军和'] else 0,
                        '[{}] 4'.format(name): wager['冠亚军和'][4] if 4 in wager['冠亚军和'] else 0,
                        '[{}] 5'.format(name): wager['冠亚军和'][5] if 5 in wager['冠亚军和'] else 0,
                        '[{}] 6'.format(name): wager['冠亚军和'][6] if 6 in wager['冠亚军和'] else 0,
                        '[{}] 7'.format(name): wager['冠亚军和'][7] if 7 in wager['冠亚军和'] else 0,
                        '[{}] 8'.format(name): wager['冠亚军和'][8] if 8 in wager['冠亚军和'] else 0,
                        '[{}] 9'.format(name): wager['冠亚军和'][9] if 9 in wager['冠亚军和'] else 0,
                        '[{}] 10'.format(name): wager['冠亚军和'][10] if 10 in wager['冠亚军和'] else 0,
                        '[{}] 11'.format(name): wager['冠亚军和'][11] if 11 in wager['冠亚军和'] else 0,
                        '[{}] 12'.format(name): wager['冠亚军和'][12] if 12 in wager['冠亚军和'] else 0,
                        '[{}] 13'.format(name): wager['冠亚军和'][13] if 13 in wager['冠亚军和'] else 0,
                        '[{}] 14'.format(name): wager['冠亚军和'][14] if 14 in wager['冠亚军和'] else 0,
                        '[{}] 15'.format(name): wager['冠亚军和'][15] if 15 in wager['冠亚军和'] else 0,
                        '[{}] 16'.format(name): wager['冠亚军和'][16] if 16 in wager['冠亚军和'] else 0,
                        '[{}] 17'.format(name): wager['冠亚军和'][17] if 17 in wager['冠亚军和'] else 0,
                        '[{}] 18'.format(name): wager['冠亚军和'][18] if 18 in wager['冠亚军和'] else 0,
                        '[{}] 19'.format(name): wager['冠亚军和'][19] if 19 in wager['冠亚军和'] else 0,
                    }
        
        return wager_dic
    
    # 获取开奖信息
    def get_season_info(self, game_name):
        """获取开奖信息"""
        
        id = self.id_table[game_name]
        driver = self.driver
        
        # 打开游戏页面
        driver.get(self.__url_item.format(id))
        
        season_num_str = "0"
        last_season_num_str = "0"
        # 等待上一期的开奖结果显示在今日开奖列表中
        print("等待上一期开奖")

        while True:
            # 等待显示有效期数
            season_num_elem = WebDriverWait(driver, 10).until(
                    element_has_valid_season_num((By.XPATH, '//*[@id="{}"]/div[2]/div/div[2]/div[1]/div/div[1]/p[2]/span'.format(id)))
                    )
            season_num_str = season_num_elem.text

            last_season_num_elem = WebDriverWait(driver, 10).until(
                    element_has_valid_season_num((By.XPATH, '//*[@id="{}"]/div[2]/div/div[3]/div[2]/div/ul[2]/li[1]/div[1]'.format(id)))
                    )
            last_season_num_str = last_season_num_elem.text
            
            if int(season_num_str) == int(last_season_num_str) + 1:
                break;
            time.sleep(1)
            self.speaker.say("正在等待")
            print(".", end="")
        
        print("")
        print("上一期已开奖")
        # 获取截止投注时间
         # 等待显示有效倒计时，秒数不是0
        season_num_elem = WebDriverWait(driver, 10).until(
                    element_has_valid_count_down((By.XPATH, '//*[@id="{}"]/div[2]/div/div[2]/div[1]/div/div[2]/span[5]'.format(id)))
                    )
        hour_str = driver.find_element_by_xpath('//*[@id="{}"]/div[2]/div/div[2]/div[1]/div/div[2]/span[1]'.format(id)).text
        hour = int(hour_str)
        minute_str = driver.find_element_by_xpath('//*[@id="{}"]/div[2]/div/div[2]/div[1]/div/div[2]/span[3]'.format(id)).text
        minute = int(minute_str)
        second_str = driver.find_element_by_xpath('//*[@id="{}"]/div[2]/div/div[2]/div[1]/div/div[2]/span[5]'.format(id)).text
        second = int(second_str)
        total_left_time = hour * 3600 + minute * 60 + second
        
        last_lottery_result = []
        last_lottery_result.append(int(last_season_num_str))
        for i in range(0, 10):
            num_str = driver.find_element_by_xpath('//*[@id="{}"]/div[2]/div/div[3]/div[2]/div/ul[2]/li[1]/div[2]/span[{}]'.format(id, 1+i)).text
            last_lottery_result.append(int(num_str))
        
        return last_lottery_result, total_left_time, season_num_str
    
    # 下注某一博彩游戏
    # game_name, 博彩游戏名称字符串，如“北京PK10”，“幸运飞艇”等
    def gamble(self, game_name, wager, limit_time_s = 60):
        """下注项目"""
        
        self.__gamble_count = 0
        print("下注{}".format(game_name))
        id = self.id_table[game_name]
        driver = self.driver
        
        # 打开游戏页面
        driver.get(self.__url_item.format(id))
        
        # 等待显示有效期数
        season_num_elem = WebDriverWait(driver, 10).until(
                    element_has_valid_season_num((By.XPATH, '//*[@id="{}"]/div[2]/div/div[2]/div[1]/div/div[1]/p[2]/span'.format(id)))
                    )
        season_num_str = season_num_elem.text
        if len(season_num_str) > 0:
            print("{}第{}期".format(game_name, season_num_str))
        else :
            raise Exception("页面信息加载错误，应显示{}第xxxxxxxxxxx期".format(game_name))
        
        # 获取截止投注时间
         # 等待显示有效倒计时，秒数不是0
        season_num_elem = WebDriverWait(driver, 10).until(
                    element_has_valid_count_down((By.XPATH, '//*[@id="{}"]/div[2]/div/div[2]/div[1]/div/div[2]/span[5]'.format(id)))
                    )
        hour_str = driver.find_element_by_xpath('//*[@id="{}"]/div[2]/div/div[2]/div[1]/div/div[2]/span[1]'.format(id)).text
        hour = int(hour_str)
        minute_str = driver.find_element_by_xpath('//*[@id="{}"]/div[2]/div/div[2]/div[1]/div/div[2]/span[3]'.format(id)).text
        minute = int(minute_str)
        second_str = driver.find_element_by_xpath('//*[@id="{}"]/div[2]/div/div[2]/div[1]/div/div[2]/span[5]'.format(id)).text
        second = int(second_str)
        print("距离截止投注时间还有：{}时{}分{}秒".format(hour, minute, second))
        
        if hour * 3600 + minute * 60 + second < limit_time_s:
            self.speaker.say("距离下注截止时间太短，暂不下注")
            print("距离下注截止时间太短，暂不下注")
            return False
        
        # 下注
        for item_num in self.name_table.keys():
            sub_wager = self.get_sub_wager(item_num, wager)
            self.gamble_sub(game_name, item_num, sub_wager)
        
        self.speaker.say("总共下注{}项".format(self.__gamble_count))
        print("总共下注{}项".format(self.__gamble_count))
        return True
    
    # 下注某一博彩游戏的项目，如冠军，亚军等
    # num, 项目的编号，0表示冠亚和，1表示冠军，2表示亚军，3表示第三名，......
    def gamble_sub(self, game_name, item_num, wager):
        id = self.id_table[game_name]
        item_name = self.name_table[item_num]
        wager_dic = wager
        if not wager_dic:
            print("不下注{}->{}".format(game_name, item_name))
            return
        
        if sum(wager_dic.values()) == 0:
            print("{}金额全为0，无需下注".format(item_name))
            return
        
        key_index_dic = self.get_item_key_index(item_num)
        
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        # 滚动页面到顶部
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        # 点击项目，如冠军
        self.wait_element_stale_and_click('//*[@id="{}"]/div[2]/div/div[3]/div[1]/nav/ul/li[{}]'.format(id, 1+item_num))
        # 点击下注条目，如[冠军]1，[冠军]2，......，[冠军]大，[冠军]小，[冠军]单，[冠军]双，[冠军]龙，[冠军]虎
        for i in range(0, len(wager_dic)):
            if wager_dic[key_index_dic[i]] > 0:
                xpath = '//*[@id="{}"]/div[2]/div/div[3]/div[1]/div[1]/div[{}]/ul/li[{}]'.format(id, 1+item_num, 1+i)
                self.wait_element_stale_and_click(xpath)
                self.__gamble_count += 1
        
        for i in range(0, len(wager_dic)):
            xpath_key = '//*[@id="{}"]/div[2]/div/div[3]/div[1]/div[2]/div[4]/div[1]/ul[{}]/li[1]'.format(id, i+1)
            xpath_value = '//*[@id="{}"]/div[2]/div/div[3]/div[1]/div[2]/div[4]/div[1]/ul[{}]/li[2]/input'.format(id, i+1)
            try:
                key_elem = driver.find_element_by_xpath(xpath_key)
                value_elem = self.wait_element_stale_and_click(xpath_value)
                value_elem.clear()
                value_elem.send_keys(str(wager_dic[key_elem.text]))
                self.speaker.say("下注{} 金额{}".format(key_elem.text, str(wager_dic[key_elem.text])))
                print("下注{} 金额{}".format(key_elem.text, str(wager_dic[key_elem.text])))
            except NoSuchElementException:
                pass
        
        # 点击立即投注 
        self.wait_element_stale_and_click('//*[@id="{}"]/div[2]/div/div[3]/div[1]/div[2]/button'.format(id))
        # 等待可再次下注
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="{}"]/div[2]/div/div[3]/div[1]/div[2]/button'.format(id))))

    def wait_result(self, game_name):
        """等待开奖结果"""
        
        print("等待{}开奖结果".format(game_name))
        id = self.id_table[game_name]
        driver = self.driver
        
        # 打开游戏页面
        driver.get(self.__url_item.format(id))
        
        # 等待显示有效期数
        season_num_elem = WebDriverWait(driver, 10).until(
                    element_has_valid_season_num((By.XPATH, '//*[@id="{}"]/div[2]/div/div[2]/div[1]/div/div[1]/p[2]/span'.format(id)))
                    )
        season_num_str = season_num_elem.text
        if len(season_num_str) > 0:
            print("{}第{}期".format(game_name, season_num_str))
        else :
            raise Exception("页面信息加载错误，应显示{}第xxxxxxxxxxx期".format(game_name))
        
        # 获取截止投注时间
        # 等待显示有效倒计时，秒数不是0
        season_num_elem = WebDriverWait(driver, 10).until(
                    element_has_valid_count_down((By.XPATH, '//*[@id="{}"]/div[2]/div/div[2]/div[1]/div/div[2]/span[5]'.format(id)))
                    )
        hour_str = driver.find_element_by_xpath('//*[@id="{}"]/div[2]/div/div[2]/div[1]/div/div[2]/span[1]'.format(id)).text
        hour = int(hour_str)
        minute_str = driver.find_element_by_xpath('//*[@id="{}"]/div[2]/div/div[2]/div[1]/div/div[2]/span[3]'.format(id)).text
        minute = int(minute_str)
        second_str = driver.find_element_by_xpath('//*[@id="{}"]/div[2]/div/div[2]/div[1]/div/div[2]/span[5]'.format(id)).text
        second = int(second_str)
        print("距离截止投注时间还有：{}时{}分{}秒".format(hour, minute, second))
        
        first_total_sec = hour * 3600 + minute * 60 + second
        total_sec = first_total_sec
        displayed_time = total_sec
        
        while total_sec != 0 and first_total_sec >= total_sec:
            if total_sec != displayed_time and total_sec % 10 == 0:
                self.speaker.say("距离截止投注时间还有：{}时{}分{}秒".format(hour, minute, second))
                print("距离截止投注时间还有：{}时{}分{}秒".format(hour, minute, second))
                displayed_time = total_sec
            time.sleep(0.5)
            hour_str = driver.find_element_by_xpath('//*[@id="{}"]/div[2]/div/div[2]/div[1]/div/div[2]/span[1]'.format(id)).text
            hour = int(hour_str)
            minute_str = driver.find_element_by_xpath('//*[@id="{}"]/div[2]/div/div[2]/div[1]/div/div[2]/span[3]'.format(id)).text
            minute = int(minute_str)
            second_str = driver.find_element_by_xpath('//*[@id="{}"]/div[2]/div/div[2]/div[1]/div/div[2]/span[5]'.format(id)).text
            second = int(second_str)
            total_sec = hour * 3600 + minute * 60 + second
        
        print("{}开奖".format(game_name)) 

    def gamble_cancel(self):
        print("撤销投注")

        driver = self.driver
        # 点击投注记录，有时候出现点击错误，用打开投注记录页面的方式代替
        #record = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="85"]/div[1]/div[1]/div/ul/li[3]/a')))
        #record.click()
        
        # 打开投注记录页面
        driver.get(self.__url_record)
        wait = WebDriverWait(driver, 10)
        
        if self.__gamble_count == 0:
            self.speaker.say("无下注，无需撤销")
            print("无下注，无需撤销")
            return

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
            xpath_game_name = '//*[@id="red"]/div/div[2]/div[2]/table/tr[{}]/td[2]'.format(i+2)
            xpath_item_name = '//*[@id="red"]/div/div[2]/div[2]/table/tr[{}]/td[4]'.format(i+2)
            xpath_money = '//*[@id="red"]/div/div[2]/div[2]/table/tr[{}]/td[7]'.format(i+2)
            try:
                # 等第一项的撤销链接刷新出来
                if i == 0:
                    wait.until(EC.presence_of_element_located((By.XPATH, xpath_cancel)))
                driver.find_element_by_xpath(xpath_cancel)
                # 等待链接所显示的位置稳定后点击
                self.wait_element_stale_and_click(xpath_cancel)
                wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[3]/button/span')))
                self.wait_element_stale_and_click('/html/body/div[2]/div/div[3]/button/span')
                print("撤销一项：{} {} 金额{}".format(driver.find_element_by_xpath(xpath_game_name).text,
                      driver.find_element_by_xpath(xpath_item_name).text,
                      driver.find_element_by_xpath(xpath_money).text))
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