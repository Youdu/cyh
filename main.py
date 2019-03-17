#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 程序运行入口

代码在python 3.7.0环境下编写
"""

from website.site_manager import SiteManager

if __name__ == '__main__':
    manager = SiteManager()
    site_chuangming = manager.create('http://cm557.com', username='lqw198421', password='lqw198421')
    login_success = site_chuangming.login(with_captcha=False)
    if not login_success:
        site_chuangming.quit()
    else:
        while True:
            wager = [
                    [0,0,0],
                    [0,0,1,0,0,
                     2,0,0,0,0,
                     1,0,0,0,0,0],
                ]
            gamble_success = site_chuangming.gamble(u'北京PK10', wager)
            if gamble_success:
                site_chuangming.gamble_cancel()
            query = input("是否等待开奖[y/n]:")
            if query is "y":
                site_chuangming.wait_result('北京PK10')
            query = input("是否继续[y/n]:")
            if query is not "y":
                site_chuangming.quit()
                break
    
    print("结束")
