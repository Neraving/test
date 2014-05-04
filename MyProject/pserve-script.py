#-*- coding: utf-8 -*-
#!D:\env\Scripts\MyProject\python.exe

__requires__ = 'pyramid==1.5'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('pyramid==1.5', 'console_scripts', 'pserve')()
    )
