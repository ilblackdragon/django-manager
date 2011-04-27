Django-template
###############

*Django-template* is python application for creating django project (instead django-admin startproject) using some specific convertions, that we use in our development process.

.. contents::

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
        + --no-git - disable git stuff
        + --no-env - disable virtual env
        + --no-langs - disable multilingual part
- Make it automaticly git repository

- Add virtualenv surround by default:
    + project_name/
        + env/
        + project/
            + project files here
            
- Make initial commit after creation (with empty dirs included (how? empty_files?))

- Super task is to update project from template, for exmaple:
    
    ./update_project my_proj - updates existing project and adds new apps\reqs\folders and stuff, without overwriting user's code

- Add full support of multilingual - from apps to folders with compiled translations for default apps
    + Multilingual flatpages
    + Database translation
    + Making and compiling translations
 
