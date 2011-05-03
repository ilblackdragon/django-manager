#!/usr/bin/env python

import os
from os.path import join, exists, abspath
import sys
import re

from __init__ import TEMPLATE_REVISION
from revision_update import DIFF_DIR

def get_parameters(filename):
    try:
        content = open(filename).read()
    except IOError:
        return None, None
    rev, args = None, None
    revs = re.findall('# REV ([0-9]*)\n', content)
    if revs:
        rev = int(revs[0])
    argss = re.findall('# ARGS ([^\n]*)\n', content)
    if argss:
        args = argss[0]
    return rev, args

def get_patch_name(rev):
    s = str(rev)
    s = "0" * (len(TEMPLATE_REVISION) - len(s)) + s
    return join(DIFF_DIR, s + '.patch')

def patch_revision(project_path, rev):
    filename = get_patch_name(rev)
    print("Appling `%s` patch" % filename)
    filename_out = filename + '.tmp'
    content = open(filename).read()
    content = content.replace("{{ project_path }}", project_path).replace("{{ arguments }}", " ")
    fout = open(filename_out, 'wb')
    fout.write(content)
    fout.close()
    curr_dir = os.getcwd()
    os.chdir(project_path)
    os.system('patch -p0 < ' + filename_out)
    os.chdir(curr_dir)
    os.remove(filename_out)

def update_project(project_path):
    project_path = abspath(project_path)
    if exists(join(project_path, 'project')):
        project_path = join(project_path, 'project')
    rev, args = get_parameters(join(project_path, '__init__.py'))
    if not rev or args is None:
        print("It not seems that project created by `Django-template` application.")
        return
    templ_rev = int(TEMPLATE_REVISION)
    if templ_rev == rev:
        print("You already have newest template revision.")
        return
    if rev > templ_rev:
        print("Your template revision newer than in django-template application. Probably you have old veriosn of application - update it.")
        return
    for r in range(rev, templ_rev):
        patch_revision(project_path, r + 1)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: ./update_project my_proj")
        exit()
    update_project(sys.argv[1])

