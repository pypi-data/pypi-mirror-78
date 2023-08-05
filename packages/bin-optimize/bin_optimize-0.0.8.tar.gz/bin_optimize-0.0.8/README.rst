|Testing| |Documentation Status| |codecov|

bin\_optimize
=============

This project is an extension to bin packing problem. The utility provides ability to optimize existing
bins which are already allocated using any bin_packing algorithm into n-1 bins.

The items in the bins are presented as a tuple of an identifier and volume of the item.

The utility is useful if there is a need to adjust items of a particular bin into remaining bins
without disturbing the contents of the remaining bins.

Installation
------------

Using pip3:

    pip3 install bin-optimize

Usage:
------

::

    >>> from bin_optimize import optimize
    >>> bins = {'b1': [('a1', 6), ('a5', 4.5), ('a9', 4)],
                'b2': [('a2', 4), ('a6', 5), ('a10', 2)],
                'b3': [('a3', 7), ('a7', 2), ('a11', 3)],
                'b4': [('a4', 2), ('a8', 2), ('a12', 2), ('a13', 2), ('a15', 4)]}
    >>> bin_to_reduce = 'b4'
    >>> optimize(bins, bin_to_reduce)
        {'b1': [('a1', 6), ('a5', 4.5), ('a9', 4), ('a8', 2)],
         'b2': [('a2', 4), ('a6', 5), ('a10', 2), ('a12', 2), ('a15', 4)],
         'b3': [('a3', 7), ('a7', 2), ('a11', 3), ('a13', 2), ('a4', 2)]}

The input bins can also have an empty bin.

::

    >>> from bin_optimize import optimize
    >>> bins = {'b1': [('a1', 6), ('a5', 4.5), ('a9', 4)],
                'b2': [('a2', 4), ('a6', 5), ('a10', 2)],
                'b3': [],
                'b4': [('a4', 2), ('a8', 2), ('a12', 2), ('a13', 2), ('a15', 4)]}
    >>> bin_to_reduce = 'b4'
    >>> optimize(bins, bin_to_reduce)
    {'b1': [('a1', 6), ('a5', 4.5), ('a9', 4)],
     'b2': [('a2', 4), ('a6', 5), ('a10', 2)],
     'b3': [('a12', 2), ('a13', 2), ('a15', 4), ('a4', 2), ('a8', 2)]}

Tests
------------
Install the test requirements:

    pip3 install -e '.[testing]'

Run the test suite from the project root using:

    flake8 && coverage run && coverage report

.. |Testing| image:: https://github.com/saripirala/bin-optimize/workflows/Testing/badge.svg?branch=master
.. |Documentation Status| image:: https://readthedocs.org/projects/bin-optimize/badge/?version=latest
   :target: https://bin-optimize.readthedocs.io/en/latest/?badge=latest
.. |codecov| image:: https://codecov.io/gh/saripirala/bin-optimize/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/saripirala/bin-optimize
