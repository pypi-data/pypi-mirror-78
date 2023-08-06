"""
@Author  : Likianta <likianta@foxmail.com>
@Module  : toolbox.py
@Created : 2019-00-00
@Updated : 2020-09-06
@Version : 0.1.3
@Desc    : 主要工具集.
    本模块用于快捷地导入主要的 utils.
    使用方法: `from lk_utils.toolbox import *`.
"""
from os.path import exists

from lk_logger import lk

from . import filesniff
from . import read_and_write
from .excel_reader import ExcelReader
from .excel_writer import ExcelWriter
from .lk_browser import browser
from .lk_config import cfg

# 将这些命名暴露到全局空间.
__all__ = [
    'ExcelReader',
    'ExcelWriter',
    'browser',
    'cfg',
    "exists",
    "filesniff",
    'lk',
    "read_and_write",
]
