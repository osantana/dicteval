dicteval
========

Library to evaluate expressions in dict/json objects.


Requirements
------------

* Python 3.6+


Basic Usage
-----------

Module ``dicteval`` will evaluate basic types with no modifications but it will
evaluate dicts (or json objects) containing keys started with ``=`` (equal)
symbol as an expression:

   >>> from dicteval import dicteval
   >>> dicteval(3)
   3
   >>> dicteval([3, 5])
   [3, 5]
   >>> dicteval((5, 3))
   [5, 3]
   >>> dicteval({"=sum": [3, 5]})
   8
   >>> dicteval({"=": 5})  # = symbol alone is a 'nop' function
   5

You can provide a dictionary with context to be used during evaluation process.

  >>> dicteval({"=": "!{var}"}, context={"var": 1.0})
  1.0

You can also wrap your string content with ``@{}`` to force a Python ``eval()``
with the context provided:

   >>> dicteval({"=sum": [3, "@{var + 2}"]}, context={"var": 3})
   8

.. warning::
   This functionality will be removed (or changed) in future releases for
   security reasons.


Functions
---------

You can use the following builtin functions in your expressions:


Function ``=any``
'''''''''''''''''

Returns ``True`` if any element of sequence is true.

    >>> dicteval({"=any": [1, 2, 3]})
    True
    >>> dicteval({"=any": [0, 0]})
    False


Function ``=eq``
''''''''''''''''

Returns ``True`` if all elements of sequence are equals:

   >>> dicteval({"=eq": [1, 1, 1, 1]})
   True


Function ``=if``
''''''''''''''''

Evaluates condition and returns first value if true, otherwise, returns second value.
If no false value is supplied, it is assumed to be ``None``.

    >>> dicteval({"=if": [{"=": "@{var > 5}"}, "yes", "no"]}, context={"var": 6})
    'yes'
    >>> dicteval({"=if": [{"=": "@{var > 5}"}, "yes", "no"]}, context={"var": 4})
    'no'
    >>> dicteval({"=if": [{"=": "@{var > 5}"}, "yes"]}, context={"var": 4})


Function ``=neq``
''''''''''''''''

Returns ``True`` if elements of sequence are different:

   >>> dicteval({"=neq": [1, 1, 1, 5]})
   True


Function ``=`` (or ``nop``)
'''''''''''''''''''''''''''

Returns the same values passed as arguments:

   >>> dicteval({"=": [1, 2, 3, 4]})
   [1, 2, 3, 4]
   >>> dicteval({"=nop": "spam"})
   'spam'


Function ``=not``
''''''''''''''''

Returns the boolean inverse of argument:

   >>> dicteval({"=not": False})
   True
   >>> dicteval({"=not": True})
   False
   >>> dicteval({"=not": None})
   True
   >>> dicteval({"=not": "XYZ"})
   False


Function ``=sum``
'''''''''''''''''

Returns a number with the sum of arguments:

   >>> dicteval({"=sum": [3, 5]})
   8


Function ``=mul``
'''''''''''''''''

Returns a number with the product of arguments:

   >>> dicteval({"=mul": [3, 5]})
   15


Function ``=all``
'''''''''''''''''

Return True if all elements of the iterable are true (or if the iterable is empty)

   >>> dicteval({"=all": (True, False)})
   False
   >>> dicteval({"=all": (True, True)})
   True


Function ``=divmod``
'''''''''''''''''

Returns a tuple containing the quotient and remainder after division:

   >>> dicteval({"=divmod": [8,3]})
   (2, 2)
   >>> dicteval({"=divmod": [7.5,2.5]})
   (3.0, 0.0)


Function ``=zip``
'''''''''''''''''

Return list of aggregate tuples constructed from elements of multiple iterables.

   >>> dicteval({"=zip": [[1, 2, 3], [4, 5], [6, 7, 8, 9]]})
   [(1, 4, 6), (2, 5, 7)]


To Do
-----

- Add more functions to the builtin language


Contribute
----------

To contribute to `dicteval`: 

    1. Clone this repository and `cd` into it
    2. Install dev dependencies with [pipenv](https://github.com/pypa/pipenv)
       ```bash
       pipenv install --dev
       ```
    3. Create a branch, like `git checkout -b [feature_name]`
    4. Git commit changes
    5. Pull request

 
License
-------

This software is licensed under MIT license.
