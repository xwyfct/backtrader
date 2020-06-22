#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
from config import LOG_PATH
from utils.logger import init_logger
import traceback

# 日志路径配置
logger = init_logger("db", LOG_PATH)


class OperateDB:
    """operate database"""

    def __init__(self, config):
        self.cursor = None
        self.db = None
        self.config = config

    # connect to db
    def connection(self):
        try:
            self.db = pymysql.connect(**self.config)
            self.cursor = self.db.cursor()
        except Exception:
            logger.error(traceback.format_exc())
            raise

    # insert or update table
    def insert_or_update(self, sql):
        try:
            self.cursor.execute(sql)
            # commit data to db
            self.db.commit()
            return 1
        except Exception:
            logger.error(traceback.format_exc())
            logger.error("sql error => %s" % sql)
            # db rollback when exists error
            self.db.rollback()
            return 0

    # insert and get insert_id
    def insert_and_get_insert_id(self, sql):
        try:
            self.cursor.execute(sql)
            insert_id = self.db.insert_id()
            self.db.commit()
            return insert_id
        except Exception:
            logger.error(traceback.format_exc())
            logger.error("sql error => %s" % sql)
            # db rollback when exists error
            self.db.rollback()
            return 0

    def execute_sql_group(self, sql_list: list):
        """用事务来执行一组sql"""
        try:
            for sql in sql_list:
                self.cursor.execute(sql)
            self.db.commit()
            return 1
        except Exception:
            self.db.rollback()
            logger.error(traceback.format_exc())
            logger.error("sql error => %s" % sql)
            return 0

    # query table
    def query(self, sql):
        """
        Input: sql
        Output: ((,..),(,..),...,(,..))
        """
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            self.db.commit()
            return results
        except Exception:
            logger.error(traceback.format_exc())
            logger.error("sql error => %s" % sql)

    # auto close db
    def __del__(self):
        self.close()

    # manual close db
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()


if __name__ == '__main__':
    # 自动发行平台系统元数据库配置
    SYS_DB_CONFIG = {
        'host': '10.155.111.136',
        'user': 'root',
        'password': 'uWtfokb42lUt',
        'port': 4000,
        'db': 'bi_publish',
        'charset': 'utf8'
    }
    db_obj = OperateMySQL(config=SYS_DB_CONFIG)
    db_obj.connection()
    for i in range(10):
        sql_insert_test = """insert into test (`name`, `age`) values('%s',%s)""" % (
            'test', i)
        re = db_obj.insert_or_update(sql_insert_test)
        # 查询新增id
        sql_id = """select max(`id`) from test;"""
        result = db_obj.query(sql=sql_id)
        max_id = result[0][0]
        print("max_id=>", max_id)
