# -*- encoding: utf-8 -*-
'''
@文件    :erro_code.py
@说明    :
@时间    :2020/09/04 11:43:13
@作者    :caimmy@hotmail.com
@版本    :0.1
'''

from enum import Enum

class KaruoFlowErrors(Enum):
    SUCCESS = 0
    ERR_UNKOWN = 1
    ERR_DATA_NOT_FOUND = 2                  # 数据记录没有在数据库查找到
    ERR_FLOW_STATUS_INVALID = 3             # 流程的状态被禁用
    ERR_FLOW_CLOSED = 4                     # 流程已结束
    ERR_FLOW_OWNER_INVALID = 5              # 非流程所有人
    ERR_DB_EXCEPTION = 6                    # 数据库异常