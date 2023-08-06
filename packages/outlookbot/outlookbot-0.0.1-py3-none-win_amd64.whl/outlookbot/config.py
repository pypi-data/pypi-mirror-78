'''
File: config.py
Created: 2020-08-28
Author: Subhendu R Mishra
'''

import os
import json


class Config:

    def __init__(self, config_file=None):
        """ Read the config file if available
        """
        self.__data = {}
        if config_file is None:
            config_file = self.__discover_config_file()

        if config_file:
            with open(config_file) as fin:
                self.__data = json.load(fin)

    def __discover_config_file(self):
        print("Discovering Config file")
        config_file_name = "config.json"
        search_locations = [os.path.join(".", config_file_name),
                            os.path.join(os.path.expanduser("~"), "outlookbot", config_file_name)]

        for file_path in search_locations:
            print(f"Checking {file_path}")
            if os.path.exists(file_path):
                print(f"Reading configurations from {file_path}")
                return file_path
        else:
            print("No config file found")

    def __getattr__(self, attr):

        return self.__data.get(attr)
