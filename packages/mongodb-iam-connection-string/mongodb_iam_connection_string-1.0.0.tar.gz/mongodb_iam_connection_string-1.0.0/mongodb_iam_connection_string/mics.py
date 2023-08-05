from os import getenv
from urllib.parse import parse_qsl, quote_plus

from boto3 import Session as boto_session
from botocore.exceptions import ClientError
from yurl import URL

from .exceptions import InvalidAWSSession


class MongoDBIAMConnectionString:
    def __init__(self, connection_string: str, profile_name: str = 'default'):
        self.creds = {}
        self.url = URL(connection_string)
        self.profile = profile_name
        self.qs = dict(parse_qsl(self.url.query))

        if self._gather_aws_creds():
            self._update_url()
        else:
            raise InvalidAWSSession

    def _gather_aws_creds(self):
        if self.profile == 'default':
            try:
                _creds = boto_session().get_credentials().get_frozen_credentials()
            except Exception:
                return False
        else:
            try:
                _creds = boto_session(
                    profile_name=self.profile).get_credentials().get_frozen_credentials()
            except Exception:
                return False

        for _ in ('access_key', 'secret_key', 'token'):
            if getattr(_creds, _):
                self.creds.update({_: str(getattr(_creds, _))})

        return True

    def _dict2qs(self, d: dict):
        return "&".join([f"{k}={v}" for k, v in d.items()])

    def _update_url(self):

        # yurl strangely parses hosts as paths, fix that
        if not self.url.host and self.url.path:
            self.url = self.url.replace(host=self.url.path, path='/')

        # Add proper protocol if not specified
        if not self.url.scheme:
            self.url = self.url.replace(scheme='mongodb+srv')

        # Add access and secret keys as username and password
        self.url = self.url.replace(
            userinfo=f"{quote_plus(self.creds['access_key'])}:{quote_plus(self.creds['secret_key'])}")

        # Set path to '/' if not provided
        if not self.url.path:
            self.url = self.url.replace(path='/')

        self.qs.update({'authSource': '$external'})
        self.qs.update({'authMechanism': 'MONGODB-AWS'})

        _token = self.creds.get('token')
        if _token:
            self.qs.update(
                {'authMechanismProperties': quote_plus(f"AWS_SESSION_TOKEN:{_token}")})

        self.url = self.url.replace(query=self._dict2qs(self.qs))

    def __repr__(self):
        return str(self.url)

    def __str__(self):
        return str(self.url)
