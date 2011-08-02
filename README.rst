######################
django-template-server
######################


Runs a server that renders Django templates.

This is intended for frontend developers and designers to be able to work with
Django templates before a backend developer/sysadmin sets up the Django project
properly.


============
Installation
============

* ``sudo pip install django-template-server``


=====
Usage
=====

* ``maketemplateserver``
* ``./runserver.py 8000``
* Open http://127.0.0.1:8000


======================
``maketemplateserver``
======================

Creates a runserver executable

Available options:

* ``-t``/``--templatedir``: Folder with your templates, defaults to ``./templates``
* ``-m``/``--mediadir``: Folder with your media (css/js) files, defaults to ``./media``
* ``-s``/``--staticdir``: Folder with your static (css/js) files, defaults to ``./static``
* ``-d``/``--django``: Django version to use, defaults to 1.3
* ``-r``/``--runserverpath``: Location where to put the runserver executable, defaults to ``./runserver.py``


================
``runserver.py``
================

Runs a server that serves templates

Available options:

* ``-l``/``--local``: Make the server only listen locally.
* A port number can be given as positional argument, defaults to the lowest open port number above 8000.
