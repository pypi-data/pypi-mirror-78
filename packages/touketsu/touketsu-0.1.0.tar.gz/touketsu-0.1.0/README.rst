.. README for touketsu package

.. image:: https://github.com/phetdam/touketsu/blob/master/doc/source/_static/
   touketsu_logo_small.png

.. image:: https://img.shields.io/travis/phetdam/touketsu?logo=travis
   :target: https://travis-ci.org/github/phetdam/touketsu
   :alt: Travis (.org)

.. image:: https://readthedocs.org/projects/touketsu/badge/?version=latest
   :target: https://touketsu.readthedocs.io/en/latest/
   :alt: Documentation Status

**touketsu** is a tiny package for creating classes that disallow dynamic
instance attribute creation or modification while preserving class inheritance.
This project was inspired by all the unfortunate incidences where fat-finger
errors led to the creation of a new instance attribute instead of the
modification of an existing instance attribute.

Installation
------------

  Note:

  Package is not on PyPI yet, but once it is, you can expect to simply use 
  ``pip`` to install.

Currently, only installing from source is available. On \*nix machines, the
recommended method is to activate a `virtual environment`__, ``cd`` to a
preferred directory, and then type

.. code:: bash

   git clone https://github.com/phetdam/touketsu
   make install

.. __: https://docs.python.org/3/tutorial/venv.html

User installation without an activated virtual environment can be performed by
replacing ``make install`` with ``make install_user``. On Windows, install in
an activated virtual environment with

.. code:: bat

   git clone https://github.com/phetdam/touketsu
   python setup.py install

Perform a user install with ``python setup.py install --user``.

After installing, check that the package is properly working using the
interpreter, for example

>>> from touketsu import immutable
>>> @immutable
... class a_class:
...     def __init__(self, a = "a"):
...         self.a = a
>>> aa = a_class()

Attempting to execute ``aa.a = 5`` will result in an ``AttributeError``, as 
``a_class`` instances are immutable.

Documentation
-------------

The documentation for ``touketsu`` is hosted on Read the Docs here__.

.. __: https://touketsu.readthedocs.io/en/latest/

