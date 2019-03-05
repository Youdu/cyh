#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 程序运行入口

代码在python 3.7.0环境下编写
"""

from website.site_manager import SiteManager

if __name__ == '__main__':
    manager = SiteManager()
    site_caiyouhui = manager.Create("http://1688552.com", username='pig', password='pigyear0214')
    site_weinisi = manager.Create("http://138nan.com")
    site_weinisi.login()
    site_weinisi.gamble_jisusaiche_a()
