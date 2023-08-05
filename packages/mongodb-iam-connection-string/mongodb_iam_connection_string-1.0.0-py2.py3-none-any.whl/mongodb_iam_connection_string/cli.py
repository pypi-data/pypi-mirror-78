#!/usr/bin/env python

"""MongoDB IAM Connection String

Usage:
  mics [--profile=default] <MONGODB_CONNECTION_STRING>

  mics (-h | --help)
  mics (-v | --version)

Options:
  --profile=AWS_PROFILE    The name of the AWS profile to use.
                           [default: default]

  -h --help                Show this screen.
  -v --version             Show version.
"""

from os import getenv
from sys import stderr

from docopt import docopt

from .exceptions import InvalidAWSSession
from .mics import MongoDBIAMConnectionString as mics


def cli():
    version = '1.0.0'
    args = docopt(__doc__, version=f"MongoDB IAM Connection String {version}")

    connection_string = args['<MONGODB_CONNECTION_STRING>']

    profile_name = getenv('AWS_PROFILE', args['--profile'])

    try:
        print(mics(connection_string=connection_string, 
                   profile_name=profile_name))
    except InvalidAWSSession:
        print('[!] Unable to load AWS session credentials.', file=stderr)
        exit(1)

    # exit successfully
    exit(0)
  
if __name__ == '__main__':
    cli()
