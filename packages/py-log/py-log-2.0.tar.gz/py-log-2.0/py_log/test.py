# -*- coding: utf-8 -*-
# @Time    : 2020/8/30 21:56
# @Author  : CC
# @Desc    : test.py
from py_log import get_logger

if __name__ == '__main__':
    logger = get_logger(__name__, log_filename='123.txt')
    logger.info('123456')
