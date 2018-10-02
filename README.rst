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
Context will be used, eg, to evaluate string objects:

  >>> dicteval({"=": "var = {var}"}, context={"var": 1})
  'var = 1'

You can also wrap your string content with ``@{}`` to force a Python ``eval()``
with the context provided:

   >>> dicteval({"=sum": [3, "@{var + 2}"]}, context={"var": 3})
   8


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

   >>> dicteval({"=divmod": [8,3])
   (2,2)
   >>> dicteval({"=divmod": [7.5,2.5]})
   (3.0,0.0)

To Do
-----

- Add more functions to the builtin language


License
-------

This software is licensed under MIT license.
