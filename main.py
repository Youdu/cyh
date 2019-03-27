#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 程序运行入口

代码在python 3.7.0环境下编写
"""

from website.site_manager import SiteManager
import airshipV4ForYou as airship
import sys, time, msvcrt
import voice
import traceback

# 这个函数在Jupyter环境下无法读取输入，只有超时会生效
def read_input(caption, default, timeout=10):
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

site_name = "创名" #"彩友会"
game_name = "幸运飞艇" # "北京PK10"
input_timeout = 5 #输入等待时间，秒
cancel_gamble = True #是否下注后取消下注，只支持创名
speaker_mute = False #是否停止语音播报
use_test_data = False #是否使用测试数据

if __name__ == '__main__':
    speaker = voice.Speaker(speaker_mute)
    manager = SiteManager()
    if site_name == "彩友会":
        site = manager.create('http://1688552.com', username='pig', password='pigyear0214', speaker = speaker)
    elif site_name == "创名":
        site = manager.create('http://cm557.com', username='lqw198421', password='lqw198421', speaker = speaker)
    else:
        print("不支持站点{}".format(site_name))
        quit()
        
    try:
        speaker.say("登录{}".format(site_name))
        login_success = site.login(with_captcha=False)
        if not login_success:
            speaker.say("登录失败，程序退出")
            site.quit()
        else:
            speaker.say("登录成功")
            while True:
#                wager = {
#                        '冠亚军和': {'冠亚大':0, '冠亚小':0, '冠亚单':0, '冠亚双':0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0},
#                        '冠军': {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, '大':0, '小':0, '龙':0, '虎':0},
#                        '亚军': {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, '大':0, '小':0, '龙':0, '虎':0},
#                        '第三名': {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, '大':0, '小':0, '龙':0, '虎':0},
#                        '第四名': {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, '大':0, '小':0, '龙':0, '虎':0},
#                        '第五名': {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, '大':0, '小':0, '龙':0, '虎':0},
#                        '第六名': {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, '大':0, '小':0, '龙':0, '虎':0},
#                        '第七名': {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, '大':0, '小':0, '龙':0, '虎':0},
#                        '第八名': {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, '大':0, '小':0, '龙':0, '虎':0},
#                        '第九名': {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, '大':0, '小':0, '龙':0, '虎':0},
#                        '第十名': {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, '大':0, '小':0, '龙':0, '虎':0},
#                        }
                if use_test_data:
                    wager = {
                            '冠亚军和': {},
                            '冠军': {6:1},
                            '亚军': {},
                            '第三名': {},
                            '第四名': {},
                            '第五名': {},
                            '第六名': {},
                            '第七名': {},
                            '第八名': {},
                            '第九名': {},
                            '第十名': {},
                            }
    
                speaker.say("等待{}上期开奖信息".format(game_name))
                last_lottery_result, left_time, season_num_str = site.get_season_info(game_name)
                print("第{}期开奖结果: ".format(last_lottery_result[0]), end="")
                print(last_lottery_result[1:11])
                
                if not use_test_data:
                    speaker.say("分析数据")
                    wager = airship.DataAnalysis(last_lottery_result)
                    print(wager)
                
                speaker.say("开始下注{}".format(game_name))
                gamble_success = site.gamble(game_name, wager)
                speaker.say("下注结束")
                
                if gamble_success:
                    if cancel_gamble:
                        speaker.say("请确认是否取消投注, {}秒后默认取消投注".format(input_timeout))
                        query = read_input("是否取消投注[y/n]:", "y", timeout=input_timeout)
                    else:
                        speaker.say("请确认是否取消投注, {}秒后默认不取消投注".format(input_timeout))
                        query = read_input("是否取消投注[y/n]:", "n", timeout=input_timeout)
                        
                    if query is "y":
                        speaker.say("取消投注")
                        site.gamble_cancel()
                        speaker.say("取消投注结束")
                        
                speaker.say("请确认是否等待开奖, {}秒后默认等待".format(input_timeout))
                query = read_input("是否等待开奖[y/n]:", "y", timeout=input_timeout)
                if query is "y":
                    speaker.say("等待开奖结果")
                    site.wait_result(game_name)
                        
                speaker.say("请确认是否继续, {}秒后默认继续".format(input_timeout))
                query = read_input("是否继续[y/n]:", "y", input_timeout)
                
                if query is not "y":
                    site.quit()
                    break
                
    except Exception:
        speaker.say("抛出异常")
        print("抛出异常：{}".format(traceback.format_exc()))        
        site.quit()
    
    speaker.say("结束")
    print("结束")
