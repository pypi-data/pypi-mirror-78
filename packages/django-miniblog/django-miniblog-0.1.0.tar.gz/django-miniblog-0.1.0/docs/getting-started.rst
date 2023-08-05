===============
Getting started
===============

miniBlog is free and open-source software, distributed under
the `Apache License 2.0 <http://www.apache.org/licenses/LICENSE-2.0>`_.
Being a reusable Django application, you will need to install Python and
Django before you can use it.

.. contents::
   :local:
   :depth: 2

----

Requirements
============

Python and Django compatibility
-------------------------------

This project requires the following:

======= ===================================
Django  Python
======= ===================================
2.2 LTS 3.5, 3.6, 3.7, 3.8 (added in 2.2.8)
------- -----------------------------------
3.1     3.6, 3.7, 3.8
======= ===================================

We highly recommend the latest release of each series for both Python and
Django.


Python virtual environment
--------------------------

It is highly recommended to install Django, miniBlog, and all other Python
dependencies of your project within
a `Python virtual environment <https://docs.python.org/3/library/venv.html>`_.

----

Install miniBlog
================

Get the latest release from PyPI
--------------------------------

This project is released on `PyPI <https://pypi.org/project/django-miniblog/>`_,
the Python Package Index. You can install the latest release with pip:

.. code-block:: bash

    pip install django-miniblog


Get the latest development version
----------------------------------

.. note::

   This option is not recommended unless you want to try incoming changes. You might
   encounter new bugs in the development version.

You can install the latest development version of this project from
the `Git repository <https://gitlab.com/pascalpepe/django-miniblog>`_:

.. code-block:: bash

    pip install git+https://gitlab.com/pascalpepe/django-miniblog.git@main#egg=django-miniblog

----

Quick start guide
=================

Settings
--------

Add ``'miniblog'`` to your ``INSTALLED_APPS`` setting:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'miniblog',
    ]

URL configuration
-----------------

Include the application URLconf in your project ``urls.py`` like this:

.. code-block:: python

    from django.urls import include, path

    urlpatterns = [
        ...
        path('blog/', include('miniblog.urls')),
    ]

Database
--------

Run ``python manage.py migrate`` to create the database tables.

Create some posts
-----------------

Start the development server and visit http://127.0.0.1:8000/admin/ to create
a post. You will need to activate the
`Django admin site <https://docs.djangoproject.com/en/dev/ref/contrib/admin/>`_
for this.

View your posts
---------------

Visit http://127.0.0.1:8000/blog/ to view a list of your posts.
