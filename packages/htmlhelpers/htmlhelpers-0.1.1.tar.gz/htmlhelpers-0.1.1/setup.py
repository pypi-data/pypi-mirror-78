# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['htmlhelpers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'htmlhelpers',
    'version': '0.1.1',
    'description': 'Simple package that helps with creating html strings.',
    'long_description': '\nhtmlhelpers\n===========\n\nA simple module for building and formatting html strings in python.\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nThis is a package which was inspired by the annoyance of writing html strings\nwhen working with serving modules like flask.\n\n.. code-block:: sh\n\n   pip install htmlhelpers\n\nBasic usage\n^^^^^^^^^^^\n\nFirst, lets make some strings with basic html elements.\n\n.. code-block:: py\n\n   from htmlhelpers import htmlstring as hs\n\nCreate an html element:\n\n.. code-block:: py\n\n   hs.p("We love volleyball!")\n   # <p>We love volleyball!</p>\n\nor one with attributes:\n\n.. code-block:: py\n\n   hs.p("We love volleyball!", attr_str=\'style="text-align:right"\')\n   # <p style="text-align:right">We love volleyball!</p>\n\nOr build a hierarchy:\n\n.. code-block:: py\n\n   hs.html(hs.p("Still love volleyball!"))\n   # <html><p>Still love volleyball!</p></html>\n\nBuild a list:\n\n.. code-block:: py\n\n   hs.ul("".join[hs.li("cats"), hs.li("dogs")])\n   # <ul><li>cats</li><li>dogs</li></ul>\n\nAlthough once a list like that begins to grow, things can start to look a little messy. For more complex html expressions, we will be using the notion on a ``tag_series`` and a ``tag_phrase``.\n\n.. code-block:: py\n\n   from htmlhelpers import htmlphrase as hp\n\nSay we have a rappidly growing list. We can use a series to quickly create many of the same html elements in succession. We can use a ``tag_series``.\n\n.. code-block:: py\n\n   list_of_animals = ["cats", "dogs", "rabbits"]\n   animals = hp.tag_series(hs.li, list_of_animals)\n   hs.ul(animals)\n   # <ul><li>cats</li><li>dogs</li><li>rabits</li></ul>\n\nAs the structure becomes deeper, we can further simplify our code with a ``tag_phrase``.\n\n.. code-block:: py\n\n   hp.tag_phrase([hs.html, hs.div, hs.ul], animals)\n   # <html><div><ul><li>cats</li><li>dogs</li><li>rabits</li></ul></div></html>\n\nLastly, you can format the string in a much more human readable way, by setting the ``formatting=True`` in the ``tag_series`` function.\n\n.. code-block:: py\n\n   hp.tag_phrase([hs.html, hs.div, hs.ul], animals, formatting=True)\n   """\n   <html>\n     <div>\n       <ul>\n         <li>cats</li>\n         <li>dogs</li>\n         <li>rabits</li>\n       </ul>\n     </div>\n   </html>\n   """\n\nOptionally, you can pass one of these html phrase strings (any multilevel heirarchy) into the ``format_phrase`` function, found in ``htmlhelpers.htmlformat`` \n\nHope this helps at least a little! :)\n',
    'author': 'steventimberman',
    'author_email': 'stevetimberman@gmail.com',
    'maintainer': 'steventimberman',
    'maintainer_email': 'stevetimberman@gmail.com',
    'url': 'https://github.com/steventimberman/htmlhelpers',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
