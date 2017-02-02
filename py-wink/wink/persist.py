import os
from ConfigParser import ConfigParser


class PersistInterface(object):
    """
    Persistence classes should implement this interface.
    """

    def load(self):
        return {}

    def save(self, data):
        pass


class ConfigFile(PersistInterface):
    """Use a config file to persist authentication information.
    """

    def __init__(self, filename="config.cfg"):
        self.filename = filename

    def load(self):
        creds = {}
        creds['username'] = os.environ['WINKUSERNAME']
        creds['client_id'] = os.environ['WINKCLIENT_ID']
        creds['access_token'] = os.environ['WINKACCESS_TOKEN']
        creds['client_secret'] = os.environ['WINKCLIENT_SECRET']
        creds['expires'] = os.environ['WINKEXPIRES']
        creds['base_url'] = os.environ['WINKBASE_URL']
        creds['refresh_token'] = os.environ['WINKREFRESH_TOKEN']
        return creds

    def save(self, creds):
        os.environ['WINKUSERNAME'] = creds['username']
        os.environ['WINKCLIENT_ID'] = creds['client_id']
        os.environ['WINKACCESS_TOKEN'] = creds['access_token']
        os.environ['WINKCLIENT_SECRET'] = creds['client_secret']
        os.environ['WINKEXPIRES'] = creds['expires']
        os.environ['WINKBASE_URL'] = creds['base_url']
        os.environ['WINKREFRESH_TOKEN'] = creds['refresh_token']
