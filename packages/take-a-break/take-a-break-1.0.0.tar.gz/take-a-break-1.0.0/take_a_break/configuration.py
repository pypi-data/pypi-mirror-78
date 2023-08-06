import logging
import os
import shutil
from configparser import ConfigParser
from os.path import expanduser

from take_a_break import get_resources

INI_FILE = ".take_a_break.ini"


def user_home():
    """
    :return: the path of the current user home
    """
    return expanduser("~")


def config_path():
    return os.path.join(user_home(), INI_FILE)


class Configuration(object):

    def __init__(self):
        if not os.path.exists(config_path()):
            logging.debug("Initialize: {} file".format(config_path()))
            shutil.copy(get_resources(INI_FILE), config_path())

        logging.debug("Reading: {} file".format(config_path()))
        self._data = ConfigParser()
        self._data.read(config_path())

    def load_resources_from_internet(self):
        return bool(self.data["default"]["load_resources_from_internet"].lower() == "true")

    def remind_me_after_this_period(self):
        return int(self.data["default"]["remind_me_after_these_minutes"]) * 60

    @property
    def data(self):
        return self._data

    def save(self):
        with open(config_path(), 'w') as configfile:
            self.data.write(configfile)


CONFIG = Configuration()
