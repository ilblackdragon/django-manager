#!/usr/bin/env python

import os
from os.path import join, exists
import sys
import re

from __init__ import TEMPLATE_REVISION

def get_parameters(filename):
    try:
        content = open(filename).read()
    except IOError:
        return None
    revs = re.findall('# REV ([0-9]*)\n', content)
    if revs:
        rev = revs[0]
    argss = re.findall('# ARGS ([^\n]*)\n', content)
    if argss:
        args = argss[0]
    return rev, args

def update_project(project_path):
    if exists(join(project_path, 'project')):
        project_path = join(project_path, 'project')
    rev, args = get_parameters(join(project_path, '__init__.py'))
    if TEMPLATE_REVISION == rev:
        print("You already have newest template revision.")
        return
    if rev > TEMPLATE_REVISION:
        print("Your template revision newer than in django-template application. Probably you have old veriosn of application - update it.")
        return
    
    print(rev, args)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: ./update_project my_proj")
        exit()
    update_project(sys.argv[1])

