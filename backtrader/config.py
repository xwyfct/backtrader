#!/usr/bin/python
# -*- coding:utf8 -*-
import os

# 自动发行平台系统元数据库配置(Tidb)
SYS_DB_CONFIG_TIDB = {
    'host': '10.155.111.136',
    # 'host': '10.155.111.236',
    'user': 'root',
    'password': 'uWtfokb42lUt',
    'db': 'bi_publish',
    'port': 4000,
    'charset': 'utf8'
}

# 自动发行平台系统元数据库配置(Mysql)，用于数据同步
SYS_DB_CONFIG_MYSQL = {
    'host': '10.173.130.114',
    # 'host': '10.155.111.236',
    'user': 'root',
    'password': 'C4YV8oTnqG',
    'db': 'bi_publish',
    'port': 3306,
    'charset': 'utf8'
}

# 使用中的自动发行平台系统元数据库配置(tidb 或者 mysql)
SYS_DB_CONFIG = SYS_DB_CONFIG_MYSQL
# SYS_DB_CONFIG = SYS_DB_CONFIG_TIDB

# tidb信号数据表连接配置
TIDB_SIGNAL_DB_CONFIG = {
    'host': '10.155.111.136',
    # 'host': '10.155.111.236',
    'user': 'root',
    'password': 'uWtfokb42lUt',
    'db': 'bi_signal',
    'port': 4000,
    'charset': 'utf8'
}

# doris信号数据表连接配置
DORIS_SIGNAL_DB_CONFIG = {
    'host': '10.143.5.249',
    'user': 'root',
    'password': 'root',
    'port': 9030,
    'db': 'bi_signal',
    'charset': 'utf8'
}
# 信号数据配置
SIGNAL_DB_CONFIG = DORIS_SIGNAL_DB_CONFIG

# doris基础数据表连接配置
BASIC_DB_CONFIG = {
    'host': '10.143.5.249',
    'user': 'root',
    'password': 'root',
    'port': 9030,
    'db': 'bi_dwb',
    'charset': 'utf8'
}
# doris信号数据映射表连接配置
SIGNAL_REFLECT_CONFIG = {
    'host': '10.143.5.249',
    'user': 'root',
    'password': 'root',
    'port': 9030,
    'db': 'bi_signal_reflect',
    'charset': 'utf8'
}

# 错误日志配置
LOG_PATH = os.path.abspath(os.path.join(os.getcwd(), "./log")) + '/backtrader.log'