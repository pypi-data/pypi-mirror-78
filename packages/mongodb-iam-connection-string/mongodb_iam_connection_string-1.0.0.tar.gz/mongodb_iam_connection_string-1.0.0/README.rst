=============================
MongoDB IAM Connection String
=============================


.. image:: https://img.shields.io/pypi/v/mongodb_iam_connection_string.svg
        :target: https://pypi.python.org/pypi/mongodb_iam_connection_string

.. image:: https://readthedocs.org/projects/mongodb-iam-connection-string/badge/?version=latest
        :target: https://mongodb-iam-connection-string.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/darrengruber/mongodb-iam-connection-string/shield.svg
     :target: https://pyup.io/repos/github/darrengruber/mongodb-iam-connection-string/
     :alt: Updates


A CLI and Python Library for configuration AWS IAM authentication with MongoDB URI connection strings.

* Documentation: https://mongodb-iam-connection-string.readthedocs.io.

Features
--------

* Adds `boto3`_'s mechanism for `loading credentials from various sources`_.
* Validates and configures the `MongoDB Connection String`_ to use `AWS IAM authentication`_ while preserving existing options.

-------
Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _`boto3`: https://github.com/boto/boto3
.. _`loading credentials from various sources`: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#configuring-credentials
.. _`MongoDB Connection String`: https://docs.mongodb.com/manual/reference/connection-string/
.. _`AWS IAM authentication`: https://docs.atlas.mongodb.com/security-add-mongodb-users/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
