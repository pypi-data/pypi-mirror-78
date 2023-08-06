=====================
News Feed Syndication
=====================
   
.. image:: https://travis-ci.org/web-sys1/NFSyndication.svg?branch=master
   :target: https://travis-ci.org/web-sys1/NFSyndication
     
This is a set of scripts for aggregating RSS feeds.

.. image:: https://repl.it/badge/github/web-sys1/NFSyndication
   :target: https://repl.it/github/web-sys1/NFSyndication

Installation
------------

You can install package through the line command:

.. code:: bash

   pip install NFSyndication

Usage
-----
Put a list of feed URLs in ``feeds.txt`` file. One feed per line. 

Run the command:

.. code:: bash

   nfsyndication-src

Assuming nothing goes wrong, the posts will be written to ``HTML`` file.

License
-------

See LICENSE_

Bug fix
-------

After many hours of working to development, it was set up an way of path
configuration due to errors. Meanwhile, we have to set code
``os.path.dirname(os.path.realpath(__file__))`` with the globalization
of variables for source code in this package. If you encounter a problem, please report `here <https://github.com/web-sys1/NFSyndication/issues/new>`_.

.. _LICENSE: https://github.com/web-sys1/NFSyndication/blob/master/LICENSE
