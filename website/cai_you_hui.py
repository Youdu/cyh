#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""彩友会站点的实现

彩友会站点有多个入口网址，其中包含http://1688552.com等
"""

from .site_base import SiteBase

class CaiYouHui(SiteBase):
    """彩友会站点
    
    """

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