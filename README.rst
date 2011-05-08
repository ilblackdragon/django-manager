Django-template
###############

*Django-template* is python application for creating django project (instead django-admin startproject) using some specific convertions, that we use in our development process.

.. contents::

Functionality
=============

- Create new django project, with folders: apps (for your applications), deploy (for deploy scripts and data), develop (for developing scripts and data), templates, static (both static and media here)
- Setup virtual enviroment
- Setup git repositort, creates first commit with all folders and than add .gitignore to ignore local_settings, deploy/lock, deploy/var/log, temprorary files and etc.
- Runs develop/update.sh that contains call for install all needed packages, including django, python-mysqld, south, django-misc.
- Update your project with new feathures from template
- Works on windows (if virtualenv and git (with all utils) installed)

Usage
=====

- To create project, type:

    ./create_project.py my_proj

- To create project in some specific directory:
    
    ./create_project.py my_proj /some/specific/directory/
    
- To update your project with new feathures fromn templates, use:
    
    ./update_project.py /path/to/your_project/


Future development
==================

- Arguments for additional configuration, for example:
    
    ./create_project my_proj --no-git

  Possible arguments:
    - --no-git - disable git stuff
    - --no-env - disable virtual env
    - --no-langs - disable multilingual part

- Make update more stable (now it very fragile). Check how update work if there are a lot of changes in project, etc.

- Add full support of multilingual - from apps to folders with compiled translations for default apps
    - Multilingual flatpages
    - Database translation
    - Making and compiling translations

