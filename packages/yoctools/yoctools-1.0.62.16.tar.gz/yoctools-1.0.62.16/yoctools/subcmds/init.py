# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function

import os
from yoctools import *

class Init(Command):
    common = True
    helpSummary = "Initialize yoc workspace in the current directory"
    helpUsage = """
%prog
"""
    helpDescription = """
Initialize yoc workspace in the current directory.
"""
    def Execute(self, opt, args):
        try:
            urlretrieve('https://yoctools.oss-cn-beijing.aliyuncs.com/yoc', '.yoc')
        except:
            pass
        if not os.path.isfile('.yoc'):
            conf = Configure()
            conf.yoc_version = 'v7.3.0'
            conf.save()
