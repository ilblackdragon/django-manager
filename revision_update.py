#!/usr/bin/env python

import os
from os.path import exists, join, dirname, abspath, isdir, isfile
import shutil
import subprocess

from __init__ import TEMPLATE_REVISION

CURRENT_DIR = dirname(abspath(__file__))

FIRST_REVISION =  '0001'
DIFF_DIR = join(CURRENT_DIR, 'diff')
TEMPLATE_PATH = join(CURRENT_DIR, 'project_name')

def initial():
    if exists(DIFF_DIR):
        return
    os.mkdir(DIFF_DIR)
    shutil.copytree(TEMPLATE_PATH, join(DIFF_DIR, FIRST_REVISION))

def get_prev_revision(rev):
    s = str(int(rev) - 1)
    s = '0' * (len(rev) - len(s)) +  s
    return s

def setup_diff_dir(path_from, path_from2, path_to):
    print("Match %s %s %s" % (path_from, path_from2, path_to))
    os.mkdir(path_to)
    files = os.listdir(path_from)
    for filename in files:
        fpath, fpath2, fpath_to = join(path_from, filename), join(path_from2, filename), join(path_to, filename)
        if isdir(fpath):
            if exists(fpath2):
                setup_diff_dir(fpath, fpath2, fpath_to)
            else:
                shutil.copytree(fpath, fpath_to)
        elif isfile(fpath):
            if exists(fpath2):
                os.system('diff ' + fpath + ' ' + fpath2 + ' -u > ' + fpath_to)
            else:
                shutil.copy(fpath, fpath_to)

def setup_diff():
    if exists(join(DIFF_DIR, TEMPLATE_REVISION)):
        print("Your revision doesn't changed")
        return
    PREV_REVISION = get_prev_revision(TEMPLATE_REVISION)
    setup_diff_dir(TEMPLATE_PATH, join(DIFF_DIR, PREV_REVISION), join(DIFF_DIR, TEMPLATE_REVISION))

def main():
    initial()
    setup_diff()

if __name__ == "__main__":
    main()
