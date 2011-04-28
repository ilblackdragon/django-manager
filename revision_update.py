#!/usr/bin/env python

import re
import os
from os.path import exists, join, dirname, abspath, isdir, isfile, basename
import shutil
import subprocess

from __init__ import TEMPLATE_REVISION

CURRENT_DIR = dirname(abspath(__file__))

DIFF_DIR = join(CURRENT_DIR, 'diff')
PREV_REVISION_PATH =  join(DIFF_DIR, 'prev')
TEMPLATE_PATH = join(CURRENT_DIR, 'project_name')

def get_revision(rev):
    s = str(rev)
    return "0" * (len(TEMPLATE_REVISION) - len(s)) + s

def modify_init_files():
    prev_init = join(PREV_REVISION_PATH, '__init__.py')
    curr_init = join(TEMPLATE_PATH, '__init__.py')
    shutil.move(prev_init, 'prev_init')
    shutil.move(curr_init, 'curr_init')
    content = open('prev_init').read()
    f = open(prev_init, 'w')
    f.write(content.replace('{{ revision }}', get_revision(int(TEMPLATE_REVISION) - 1)))
    f.close()
    content = open('curr_init').read()
    f = open(curr_init, 'w')
    f.write(content.replace('{{ revision }}', TEMPLATE_REVISION))
    f.close()

def return_init_files():
    shutil.move('prev_init', prev_init)
    shutil.move('curr_init', curr_init)
    
def main():
    if not exists(PREV_REVISION_PATH):
        if not exists(DIFF_DIR):
            os.mkdir(DIFF_DIR)
        shutil.copytree(TEMPLATE_PATH, PREV_REVISION_PATH)
    if exists(join(DIFF_DIR, TEMPLATE_REVISION)):
        print("Your revision doesn't changed")
        return

    # Get patch
    modify_init_files()
    res_file = join(DIFF_DIR, TEMPLATE_REVISION) + '.patch'
    temp_file = res_file + '.tmp'
    os.system('diff -rupN ' + PREV_REVISION_PATH + ' ' + TEMPLATE_PATH + ' > ' + temp_file)
    return_init_files()
    
    # Update patch
    content = open(temp_file).read()
    content = content.replace(TEMPLATE_PATH, '{{ project_path }}')
    content = content.replace(DIFF_DIR, basename(DIFF_DIR))
    fout = open(res_file, 'wb')
    fout.write(content)
    fout.close()
    os.remove(temp_file)

    # Update previsous version to current
    shutil.rmtree(PREV_REVISION_PATH)
    shutil.copytree(TEMPLATE_PATH, PREV_REVISION_PATH)

if __name__ == "__main__":
    main()
