
htmlhelpers
===========

A simple module for building and formatting html strings in python.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a package which was inspired by the annoyance of writing html strings
when working with serving modules like flask.

.. code-block:: sh

   pip install htmlhelpers

Basic usage
^^^^^^^^^^^

First, lets make some strings with basic html elements.

.. code-block:: py

   from htmlhelpers import htmlstring as hs

Create an html element:

.. code-block:: py

   hs.p("We love volleyball!")
   # <p>We love volleyball!</p>

or one with attributes:

.. code-block:: py

   hs.p("We love volleyball!", attr_str='style="text-align:right"')
   # <p style="text-align:right">We love volleyball!</p>

Or build a hierarchy:

.. code-block:: py

   hs.html(hs.p("Still love volleyball!"))
   # <html><p>Still love volleyball!</p></html>

Build a list:

.. code-block:: py

   hs.ul("".join[hs.li("cats"), hs.li("dogs")])
   # <ul><li>cats</li><li>dogs</li></ul>

Although once a list like that begins to grow, things can start to look a little messy. For more complex html expressions, we will be using the notion on a ``tag_series`` and a ``tag_phrase``.

.. code-block:: py

   from htmlhelpers import htmlphrase as hp

Say we have a rappidly growing list. We can use a series to quickly create many of the same html elements in succession. We can use a ``tag_series``.

.. code-block:: py

   list_of_animals = ["cats", "dogs", "rabbits"]
   animals = hp.tag_series(hs.li, list_of_animals)
   hs.ul(animals)
   # <ul><li>cats</li><li>dogs</li><li>rabits</li></ul>

As the structure becomes deeper, we can further simplify our code with a ``tag_phrase``.

.. code-block:: py

   hp.tag_phrase([hs.html, hs.div, hs.ul], animals)
   # <html><div><ul><li>cats</li><li>dogs</li><li>rabits</li></ul></div></html>

Lastly, you can format the string in a much more human readable way, by setting the ``formatting=True`` in the ``tag_series`` function.

.. code-block:: py

   hp.tag_phrase([hs.html, hs.div, hs.ul], animals, formatting=True)
   """
   <html>
     <div>
       <ul>
         <li>cats</li>
         <li>dogs</li>
         <li>rabits</li>
       </ul>
     </div>
   </html>
   """

Optionally, you can pass one of these html phrase strings (any multilevel heirarchy) into the ``format_phrase`` function, found in ``htmlhelpers.htmlformat`` 

Hope this helps at least a little! :)
