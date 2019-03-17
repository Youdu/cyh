#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 程序运行入口

代码在python 3.7.0环境下编写
"""

from website.site_manager import SiteManager
import airshipV4ForYou as airship
import sys, time, msvcrt

def read_input(caption, default, timeout=5):
    start_time = time.time()
    sys.stdout.write('%s(%d秒自动跳过):' % (caption,timeout))
    sys.stdout.flush()
    input = ''
    while True:
        ini=msvcrt.kbhit()
        try:
            if ini:
                chr = msvcrt.getche()
                if ord(chr) == 13:  # enter_key
                    break
                elif ord(chr) >= 32:
                    input += chr.decode()
        except Exception:
            pass
        if len(input) == 0 and time.time() - start_time > timeout:
            break
    print ('')  # needed to move to next line
    if len(input) > 0:
        return input+''
    else:
        return default


if __name__ == '__main__':
    manager = SiteManager()
    site_chuangming = manager.create('http://cm557.com', username='lqw198421', password='lqw198421')
    login_success = site_chuangming.login(with_captcha=False)
    if not login_success:
        site_chuangming.quit()
    else:
        while True:
#            wager = {
#                    '冠亚军和': {'冠亚大':1, '冠亚小':2, '冠亚单':0, '冠亚双':0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0},
#                    '冠军': {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, '大':0, '小':0, '龙':0, '虎':0},
#                    '亚军': {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, '大':0, '小':0, '龙':0, '虎':0},
#                    '第三名': {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, '大':0, '小':0, '龙':0, '虎':0},
#                    '第四名': {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, '大':0, '小':0, '龙':0, '虎':0},
#                    '第五名': {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, '大':0, '小':0, '龙':0, '虎':0},
#                    '第六名': {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, '大':0, '小':0, '龙':0, '虎':0},
#                    '第七名': {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, '大':0, '小':0, '龙':0, '虎':0},
#                    '第八名': {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, '大':0, '小':0, '龙':0, '虎':0},
#                    '第九名': {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, '大':0, '小':0, '龙':0, '虎':0},
#                    '第十名': {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, '大':0, '小':0, '龙':0, '虎':0},
#                    }

            last_lottery_result, left_time, season_num_str = site_chuangming.get_season_info('北京PK10')
            print("第{}期开奖结果: ".format(last_lottery_result[0]), end="")
            print(last_lottery_result[1:11])
            wager = airship.DataAnalysis(last_lottery_result)
            print(wager)
            gamble_success = site_chuangming.gamble('北京PK10', wager)
            if gamble_success:
                site_chuangming.gamble_cancel()
            query = read_input("是否等待开奖[y/n]:", "y")
            if query is "y":
                site_chuangming.wait_result('北京PK10')
            query = read_input("是否继续[y/n]:", "y")
            if query is not "y":
                site_chuangming.quit()
                break
    
    print("结束")
