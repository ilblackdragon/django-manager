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

Usage
=====

- To create project, type:

    ./create_project.py my_proj

- To create project in some specific directory:
    
    ./create_project.py my_proj /some/specific/directory/
    

Future development
==================

- Arguments for additional configuration, for example:
    
    ./create_project my_proj --no-git

  Possible arguments:
    - --no-git - disable git stuff
    - --no-env - disable virtual env
    - --no-langs - disable multilingual part

- Super task is to update project from template, for exmaple:
    
    ./update_project my_proj - updates existing project and adds new apps\reqs\folders and stuff, without overwriting user's code

  Nice idea, is to have diff patches from all template revisions to current. So when update_project is calling, it figure out project's revision and then apply patches.

- Add full support of multilingual - from apps to folders with compiled translations for default apps
    - Multilingual flatpages
    - Database translation
    - Making and compiling translations
 
