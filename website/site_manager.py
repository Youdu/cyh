#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""站点管理类的实现

这个模块定义站点管理类.，用于创建各个站点。
"""

from .cai_you_hui import CaiYouHui
from .wei_ni_si import WeiNiSi
from .chuang_ming import ChuangMing

class SiteManager:
    """站点管理类
    
    """
    
    site_map = {
            'http://1688552.com': CaiYouHui,
            'http://138nan.com': WeiNiSi,
            'http://cm557.com': ChuangMing,
            }

    def __init__(self, *args, **kwargs):
        pass
    
    def create(self, url, *args, **kwargs):
        """由url地址创建对应的站点"""
        
        try:
            site_type = self.site_map[url]
        except KeyError:
            raise Exception("找不到站点{}的实现".format(url))

        site = site_type(url, *args, **kwargs)
        
        return site
    
