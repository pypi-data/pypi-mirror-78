nbpretty
========

nbpretty is a tool to convert sets of notebook files into a single, cohesive set of linked pages.

Usage
-----

Create a file called ``config.yaml`` with the following contents:

.. code-block:: yaml

   ---
   course_title: Best practices in software engineering

The main pages will be created bases on their names.
You should name your chapters like: ``00 Introduction.ipynb``, ``01 First Chapter.ipynb`` etc.

and then run it with:

.. code-block:: shell-session

   nbpretty .

It will write out HTML and CSS files which can then be uploaded/viewed/whatever.

For development, I recommend using `entr <http://eradman.com/entrproject/>`_ with:

.. code-block:: shell-session

   while sleep 1 ; do find . -name '*.ipynb' | entr -d nbpretty . ; done
