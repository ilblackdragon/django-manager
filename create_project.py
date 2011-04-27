#!/usr/bin/env python

import os
from os.path import dirname, basename, join, isdir, isfile
import sys
import shutil
import string
from random import choice
 

PROJECT_TEMPLATE_PATH = join(dirname(__file__), 'project_name')

def secret_key():
    return ''.join([choice(string.letters + string.digits + string.punctuation) for i in range(50)])


def copy_tree(path_from, path_to, args):

    def handle_string(string, args, brackets=False):
        for arg in args:
            string = string.replace("{{ " + arg + " }}" if brackets else arg, args[arg])
        return string

    def copy_file(filename_from, filename_to):
        content = open(filename_from, 'r').read()
        fout = open(filename_to, 'wb')
        fout.write(handle_string(content, args, True))
        fout.close()

    os.mkdir(path_to)
    files = os.listdir(path_from)
    for f in files:
        fpath = join(path_from, f)
        fpath_to = join(path_to, handle_string(f, args))
        if isdir(fpath):
            copy_tree(fpath, fpath_to, args)
        elif isfile(fpath):
            if f != "empty_file":
                copy_file(fpath, fpath_to)
        else:
            print("Can't copy `%s` - not yet implemented." % fpath)

def create_project(project_name, project_path):
    project_to = join(project_path, project_name)
    if os.path.exists(project_to):
        print("`%s` already exists. Please choose another project name or path" % project_to)
        return
    try:
        __import__(project_name)
    except ImportError:
        pass
    else:
        print("`%s` confilcts with the name of an existing Python module and cannot be used as project name. Please choose another project name" % project_name)
        return
    try:    
        copy_tree(PROJECT_TEMPLATE_PATH, join(project_to), {
            'project_name': project_name,
            'Project_name': project_name.capitalize(),
            'secret_key': secret_key(),
        })
    except Exception as e:
        shutil.rmtree(project_to)
        raise e

if __name__ == "__main__":
    # TODO: Add arg parse for additional configuration
    if len(sys.argv) not in [2, 3]:
        print("Usage: create_project.py project_name [project_path]")
        exit()
    if len(sys.argv) == 3:
        project_path = sys.argv[3]
    else:
        project_path = os.getcwd()
    create_project(sys.argv[1], project_path)

