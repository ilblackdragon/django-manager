#!/usr/bin/env python

import os
from os.path import dirname, basename, join, isdir, isfile
import sys
import shutil
import subprocess
import string
from random import choice
 

PROJECT_TEMPLATE_PATH = join(dirname(__file__), 'project_name')
ENV_DIR = 'env'
ENV_PROJECT_DIR = 'project'

def secret_key():
    return ''.join([choice(string.letters + string.digits + string.punctuation) for i in range(50)])

def setup_virtual_env(path_to):
    os.mkdir(path_to)
    subprocess.call(['virtualenv', join(path_to, ENV_DIR)])

def setup_git(path_to):
    cur_dir = os.getcwd()
    os.chdir(path_to)
    subprocess.call(['git', 'init', '.'])
    subprocess.call(['git', 'add', '-A'])
    subprocess.call(['git', 'commit', '-m', '"Initial commit"'])
    os.chdir(cur_dir)

def apps_install(path_to):
    cur_dir = os.getcwd()
    os.chdir(path_to)
    subprocess.call(['./develop/update.sh'])
    os.chdir(cur_dir)

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
        attr = os.stat(filename_from)
        os.chmod(filename_to, attr.st_mode)

    def get_paths(filename, path_from, path_to):
        if filename == "empty_file":
            return (None, None)
        elif filename == "gitignore":
            return (join(path_from, filename), join(path_to, '.' + filename))
        return (join(path_from, filename), join(path_to, filename))

    os.mkdir(path_to)
    files = os.listdir(path_from)
    for filename in files:
        fpath, fpath_to = get_paths(filename, path_from, path_to)
        if not fpath or not fpath_to:
            continue
        if isdir(fpath):
            copy_tree(fpath, fpath_to, args)
        elif isfile(fpath):
            copy_file(fpath, fpath_to)
        else:
            print("Can't copy `%s` - not yet implemented for this file type." % fpath)

def create_project(project_name, project_path, enable_env=True, enable_git=True, enable_apps_install=True):
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
        if enable_env:
            setup_virtual_env(project_to)
            project_to = join(project_to, ENV_PROJECT_DIR)
        copy_tree(PROJECT_TEMPLATE_PATH, project_to, {
            'project_name': project_name,
            'Project_name': project_name.capitalize(),
            'secret_key': secret_key(),
        })
        if enable_git:
            setup_git(project_to)
        if enable_apps_install:
            apps_install(project_to)
    except Exception as e:
        if os.path.exists(project_to):
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

