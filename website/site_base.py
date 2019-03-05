#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""站点基类的实现

这个模块定义站点基类. 
定义通用的属性：用户名，密码，站点cookies等
定义通用的方法：登陆，获取帐户信息，下注等
"""

class SiteBase:
    """站点基类
    
    """

    def __init__(self, *args, **kwargs):
        try:
            self.username = kwargs['username']
            self.password = kwargs['password']
        except KeyError as err:
            raise Exception("参数缺失{}".format(err))
