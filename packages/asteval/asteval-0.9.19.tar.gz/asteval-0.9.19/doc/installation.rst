====================================
Downloading and Installation
====================================

.. _numpy: http://docs.scipy.org/doc/numpy
.. _github:  http://github.com/newville/asteval
.. _PyPI:  http://pypi.python.org/pypi/asteval/

Requirements
~~~~~~~~~~~~~~~

Asteval is a pure python module with no required dependencies outside of the
standard library.  Asteval will make use of the `numpy`_ module if
available.  The test suite requires the `pytest` module. 

Version 0.9.19 supports and is tested with Python 3.6 through 3.8. Support
for Python 3.5 was not deliberately broken, but testing for this version
has now stopped, and development going forward will assume Python3.6+.

This version also includes changes to work with Python 3.9beta, and all
tests pass locally. Python 3.9 is not yet tested automatically, and some
issues may arise with this version.

Version 0.9.18 supported and was tested with Python 3.5 through 3.8.

Version 0.9.17 was the last version to support Python 2.7.


Download and Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The latest stable version of asteval is |release| and is available at
`PyPI`_ or as a conda package.  You should be able to install asteval
with::

   pip install asteval

or::

   conda install -c GSECARS asteval

Development Version
~~~~~~~~~~~~~~~~~~~~~~~~

The latest development version can be found at the `github`_ repository, and cloned with::

    git clone http://github.com/newville/asteval.git


Installation
~~~~~~~~~~~~~~~~~

Installation from source on any platform is::

   python setup.py install

License
~~~~~~~~~~~~~

The ASTEVAL code is distribution under the following license:

.. literalinclude:: ../LICENSE
