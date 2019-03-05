#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""威尼斯彩乐园站点的实现

威尼斯彩乐园站点的入口地址是http://138nan.com
"""

from .site_base import SiteBase

class WeiNiSi(SiteBase):
    """威尼斯彩乐园站点
    
    """

    def __init__(self, *args, **kwargs):
        print("WeiNiSi初始化")
        try:
            super().__init__(self, *args, **kwargs)
        except Exception as err:
            print("{}。将以游客身份登陆".format(err))
            self.login_as_visitor = True
    
    def login(self):
        if self.login_as_visitor:
            pass
        
    def get_acount_info(self):
        pass

        