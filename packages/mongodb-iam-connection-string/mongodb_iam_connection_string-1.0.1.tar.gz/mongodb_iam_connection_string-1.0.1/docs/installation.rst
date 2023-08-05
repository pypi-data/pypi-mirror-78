.. highlight:: shell

============
Installation
============


Stable release
--------------

To install MongoDB IAM Connection String as CLI tool, it is recommended that you use `pipx`_ to install this utility within its own virtualenv.

.. code-block:: console

    $ pipx install mongodb-iam-connection-string

This is the preferred method to install MongoDB IAM Connection String, as it will always install the most recent stable release.

If you don't have `pipx`_ installed, this `pipx installation guide`_ can guide
you through the process.

.. _pipx: https://github.com/pipxproject/pipx
.. _pipx installation guide: https://pipxproject.github.io/pipx/installation/


From sources
------------

The sources for MongoDB IAM Connection String can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/darrengruber/mongodb-iam-connection-string

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/darrengruber/mongodb-iam-connection-string/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/darrengruber/mongodb-iam-connection-string
.. _tarball: https://github.com/darrengruber/mongodb-iam-connection-string/tarball/master
