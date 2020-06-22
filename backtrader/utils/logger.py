#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from logging import Logger, Manager, PlaceHolder, _acquireLock, _releaseLock, root, ERROR
from logging.handlers import TimedRotatingFileHandler
# import time
# import os
# import fcntl
# from config import DD_ALERT_CONFIG
from utils.dingding import DdAlert


# 重写Logger.error方法实现记录错误日志同时往钉钉发送错误信息
class MyLogger(Logger):

    def error(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'ERROR'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.error("Houston, we have a %s", "major problem", exc_info=1)
        """
        if self.isEnabledFor(ERROR):
            self.push_error_to_media(msg)
            self._log(ERROR, msg, args, **kwargs)
        

    def push_error_to_media(self, msg):
        """发送错误消息至第三方"""
        dd_alert = DdAlert("server")
        dd_alert.msg_alert(msg)


class MyManager(Manager):

    def getLogger(self, name):
        """
        Get a logger with the specified name (channel name), creating it
        if it doesn't yet exist. This name is a dot-separated hierarchical
        name, such as "a", "a.b", "a.b.c" or similar.

        If a PlaceHolder existed for the specified name [i.e. the logger
        didn't exist but a child of it did], replace it with the created
        logger and fix up the parent/child references which pointed to the
        placeholder to now point to the logger.
        """
        rv = None
        if not isinstance(name, str):
            raise TypeError('A logger name must be a string')
        _acquireLock()
        try:
            if name in self.loggerDict:
                rv = self.loggerDict[name]
                if isinstance(rv, PlaceHolder):
                    ph = rv
                    # rv = (self.loggerClass or _loggerClass)(name)
                    rv = (self.loggerClass or MyLogger)(name)
                    rv.manager = self
                    self.loggerDict[name] = rv
                    self._fixupChildren(ph, rv)
                    self._fixupParents(rv)
            else:
                rv = (self.loggerClass or MyLogger)(name)
                rv.manager = self
                self.loggerDict[name] = rv
                self._fixupParents(rv)
        finally:
            _releaseLock()
        return rv


def MyGetLogger(name=None):
    """
    Return a logger with the specified name, creating it if necessary.

    If no name is specified, return the root logger.
    """
    if name:
        return MyManager(root).getLogger(name)
    else:
        return root


# 重写TimedRotatingFileHandler中类方法doRollover，兼容多进程并发日志滚动记录。
# class MultiCompatibleTimedRotatingFileHandler(TimedRotatingFileHandler):

#     def doRollover(self):
#         if self.stream:
#             self.stream.close()
#             self.stream = None
#         # get the time that this sequence started at and make it a TimeTuple
#         currentTime = int(time.time())
#         dstNow = time.localtime(currentTime)[-1]
#         t = self.rolloverAt - self.interval
#         if self.utc:
#             timeTuple = time.gmtime(t)
#         else:
#             timeTuple = time.localtime(t)
#             dstThen = timeTuple[-1]
#             if dstNow != dstThen:
#                 if dstNow:
#                     addend = 3600
#                 else:
#                     addend = -3600
#                 timeTuple = time.localtime(t + addend)
#         dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)
#         # 兼容多进程并发 LOG_ROTATE
#         if not os.path.exists(dfn):
#             f = open(self.baseFilename, 'a')
#             fcntl.lockf(f.fileno(), fcntl.LOCK_EX)
#             if not os.path.exists(dfn):
#                 os.rename(self.baseFilename, dfn)
#             # 释放锁 释放老 log 句柄
#             f.close()
#         if self.backupCount > 0:
#             for s in self.getFilesToDelete():
#                 os.remove(s)
#         if not self.delay:
#             self.stream = self._open()
#         newRolloverAt = self.computeRollover(currentTime)
#         while newRolloverAt <= currentTime:
#             newRolloverAt = newRolloverAt + self.interval
#         # If DST changes and midnight or weekly rollover, adjust for this.
#         if (self.when == 'MIDNIGHT' or
#                 self.when.startswith('W')) and not self.utc:
#             dstAtRollover = time.localtime(newRolloverAt)[-1]
#             if dstNow != dstAtRollover:
#                 if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
#                     addend = -3600
#                 else:  # DST bows out before next rollover, so we need to add an hour
#                     addend = 3600
#                 newRolloverAt += addend
#         self.rolloverAt = newRolloverAt


def init_logger(logger_name, log_path):
    # if logger_name not in Logger.manager.loggerDict:
    logger = MyGetLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # Log等级总开关
    handler = TimedRotatingFileHandler(log_path,
                                       when='midnight',
                                       interval=1,
                                       backupCount=12,
                                       encoding='utf-8')
    # handler = MultiCompatibleTimedRotatingFileHandler(log_path,
    #                                                   when='midnight',
    #                                                   interval=30,
    #                                                   backupCount=12,
    #                                                   encoding='utf-8')
    datefmt = "%Y-%m-%d %H:%M:%S"
    format_str = "[%(asctime)s]: %(name)s %(levelname)s %(lineno)s %(message)s"
    formatter = logging.Formatter(format_str, datefmt)
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)  # 输出到file的log等级的开关
    logger.addHandler(handler)
    return logger


if __name__ == '__main__':
    logger = init_logger("test", './test.log')
    logger.error("this is test message")
