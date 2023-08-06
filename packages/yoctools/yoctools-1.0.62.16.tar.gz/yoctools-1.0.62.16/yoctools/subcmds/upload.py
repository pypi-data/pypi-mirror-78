# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function
from yoctools import *


class Upload(Command):
    common = True
    helpSummary = "Upload component to OCC"
    helpUsage = """
%prog [option] [<component>...]
"""
    helpDescription = """
upload component to OCC
"""

    def _Options(self, p):
        p.add_option('-g', '--git',
                     dest='update_git', action='store_true',
                     help='upload code to git repo')
        p.add_option('-o', '--occ',
                     dest='update_occ', action='store_true',
                     help='upload code to OCC')


    def Execute(self, opt, args):
        if not (opt.update_git or opt.update_occ):
            self.Usage()
            return

        yoc = YoC()
        count = len(args)
        if opt.update_git:
            repo = RepoGitee(yoc.conf.gitee_token)
            if repo:
                if count == 0:
                    put_string("Uploading all components, please wait...")
                flag = False
                for component in yoc.components:
                    if component.name in args or count == 0:
                        if count > 0:
                            flag = True
                        component.load_package()
                        ssh_url = repo.create_project(
                            component.name, component.json_dumps())
                        if ssh_url:
                            put_string("Uploading %s, please wait..." % component.name)
                            component.upload()
                            put_string("Upload %s finish." % component.name)
                        else:
                            put_string("Upload %s failed!" % component.name)
                if not flag:
                    put_string("Can't find components:%s!" % str(args))
            else:
                put_string("Connect git repo error!")

        if opt.update_occ:
            if count == 0:
                put_string("Uploading all components, please wait...")
                yoc.uploadall()
            else:
                for name in args:
                    put_string("Start to upload component:%s to OCC." % name)
                    yoc.upload(name)
