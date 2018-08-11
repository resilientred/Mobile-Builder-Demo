import fileinput
import re

# This class parse and replace value in AppParams by key
from builder.lib.model.entity.driver_app import DriverApplication


HOST = "HOST"
HOST_NEW = "HOST_NEW"
CHAT_SERVER = "CHAT_SERVER"
URL_GEOCODE = "URL_GEOCODE"
TENANT = "TENANT"
VERSION_APP = "VERSION_APP"
SENDER_ID = "SENDER_ID"
APP_VERSION = "VERSION_APP"
TYPE_APP = "TYPE_APP"


class AndroidDriverConfigurator:

    def __init__(self, file_path):
        self.file_path = file_path


    # FIND REGEX
    @staticmethod
    def regex_psfs(key):
        return '^.*\s' + key + '\s=\s\"([^\"]+)\".*$'


    @staticmethod
    def regex_obj(key):
        return '^.*\s' + key + '\s*=\s*([^;]+).*$'


    # FIND FUNCTIONS
    def find_psfs(self, text, key):
        return re.findall(self.regex_psfs(key), text, flags=re.MULTILINE)


    def find_obj(self, text, key):
        return re.findall(self.regex_obj(key), text, flags=re.MULTILINE)


    # PUT FUNCTIONS
    def put_string(self, key, new):
        with fileinput.FileInput(self.file_path, inplace=True) as file:
            for line in file:
                group = self.find_psfs(line, key)
                if len(group) > 0:
                    print(line.replace(group[0], str(new)), end='')
                else:
                    print(line, end='')


    def put_obj(self, key, new):
        with fileinput.FileInput(self.file_path, inplace=True) as file:
            for line in file:
                group = self.find_obj(line, key)
                if len(group) > 0:
                    print(line.replace(group[0], str(new)), end='')
                else:
                    print(line, end='')


    def put_bool(self, key, new):
        with fileinput.FileInput(self.file_path, inplace=True) as file:
            for line in file:
                group = self.find_obj(line, key)
                if len(group) > 0:
                    print(line.replace(group[0], str(new).lower()), end='')
                else:
                    print(line, end='')

    # CONFIGURABLE BY APPLICATION
    def configure_by_app(self, config: DriverApplication):
        self.put_string(TENANT, config.tenant_name)
        self.put_string(HOST, config.host)
        self.put_string(HOST_NEW, config.new_host)
        self.put_string(CHAT_SERVER, config.chat_host)
        self.put_string(URL_GEOCODE, config.geocode_host)
        self.put_string(SENDER_ID, config.push_key)
        self.put_obj(TYPE_APP, config.app_type)
        self.put_obj(APP_VERSION, config.version_app)
