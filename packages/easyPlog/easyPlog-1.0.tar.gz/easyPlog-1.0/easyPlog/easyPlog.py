"""
@author: yangqiang
@contact: whuhit09@gmail.com
@file: Plog.py
@time: 2020-04-27 17:48
"""
import pathlib
import logging
import uuid
from logging.handlers import TimedRotatingFileHandler
import time


class Plog(object):
    """
    docstring for Plog
    """
    formatter = logging.Formatter(fmt='[%(asctime)s.%(msecs)03d] [%(levelname)08s] [%(lineno)03s]: %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    formatter2 = logging.Formatter('%(message)s')

    def __init__(self, log_file, level=logging.DEBUG, stream=False, msgOnly=True, cover=False):
        """
        stream  :  是否同步终端输出日志
        msgOnly :  record details or not
        cover  : 表示是否覆盖之前的文件
        """

        pdir = pathlib.Path(log_file).parent
        if not pdir.exists():
            pathlib.Path.mkdir(pdir, parents=True)  #
        self.log_file = log_file
        if cover and pathlib.Path(self.log_file).exists():
            pathlib.Path(self.log_file).unlink()
        self.level = level
        self.stream = stream
        self.log_name = str(uuid.uuid1())  #

        self.logger = logging.getLogger(self.log_name)
        self.logger.setLevel(self.level)

        # file
        handler = TimedRotatingFileHandler(self.log_file, when='D', encoding="utf-8")
        if msgOnly:
            handler.setFormatter(Plog.formatter2)
        else:
            handler.setFormatter(Plog.formatter)
        self.logger.addHandler(handler)

        # stream
        if self.stream:
            streamHandler = logging.StreamHandler()
            streamHandler.setFormatter(Plog.formatter2)
            self.logger.addHandler(streamHandler)

        if not cover:
            self.logger.debug(f"==========***** {time.strftime('%Y-%m-%d %H:%M:%S')} start to log *****==========")

    def __getattr__(self, item):
        return getattr(self.logger, item)

    def log(self, *args):
        msg = ''
        for arg in args:
            msg = f"{msg} {repr(arg)}"
        self.logger.debug(msg.lstrip(' '))

    def debug(self, *args):
        self.log(*args)

    def info(self, *args):
        msg = ''
        for arg in args:
            msg = f"{msg} {repr(arg)}"
        self.logger.info(msg.lstrip(' '))


if __name__ == '__main__':
    log = Plog('f.log', msgOnly=False)
    log.log("fas", 12, [23, 4, 5], set(), {'sf': 9})
    log.info("fas", 12, [23, 4, 5], set(), {'sf': 9})
