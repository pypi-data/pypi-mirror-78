# -*- encoding: utf-8 -*-
'''
@文件    :datadef.py
@说明    :
@时间    :2020/09/02 21:54:28
@作者    :caimmy@hotmail.com
@版本    :0.1
'''

from dataclasses import dataclass

@dataclass
class DbConfig:
    """
    数据库的配置参数
    """
    host: str
    dbname: str
    user: str
    password: str
    port: int = 3306

    pool_size: int = 100
    pool_recycle: int = 600