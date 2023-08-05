=====
Usage
=====

To use MongoDB IAM Connection String as a CLI tool:

.. code-block:: console

    $ mongo $(mics 'mycluster.5mha8.mongodb.net')

To use MongoDB IAM Connection String in a project::

    # import the class
    from mongodb_iam_connection_string import MongoDBIAMConnectionString

    # generate a connection string
    cluster_address = 'mycluster.5mha8.mongodb.net'
    try:
        mongodb_connection_string = str(MongoDBIAMConnectionString(cluster_address))
    except InvalidAWSSession:
        # handle this exception
        pass

