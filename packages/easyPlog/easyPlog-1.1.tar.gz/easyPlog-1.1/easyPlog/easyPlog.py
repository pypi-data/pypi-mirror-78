"""
@author: yangqiang
@contact: whuhit2020@gmail.com
@file: easyPlog.py
@time: 2020/4/3 14:50
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
    formatter = logging.Formatter(fmt='[%(asctime)s.%(msecs)03d] [%(levelname)08s]: %(message)s',
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

    def _msgRecombine(self, *args):
        msg = ""
        for arg in args:
            if isinstance(arg, str):
                msg = f"{msg} {arg}"
            else:
                msg = f"{msg} {repr(arg)}"
        return msg.lstrip(' ')

    def log(self, *args):
        self.logger.debug(self._msgRecombine(*args))

    def debug(self, *args):
        self.log(*args)

    def info(self, *args):
        self.logger.info(self._msgRecombine(*args))

    def error(self, *args):
        self.logger.error(self._msgRecombine(*args))

    def warning(self, *args):
        self.logger.warning(self._msgRecombine(*args))
