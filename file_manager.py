#!/usr/bin/env python3

# General-purpose dependencies
from enum import Enum
import json
import sys
import argparse


class FileManager():
    def __init__(self):
        self.start_time = 0

    def check_path_is_correct(self, filename):
        try:
            with open(filename, 'w') as file:
                pass
        except FileNotFoundError:
            print("Sorry, the file "+ filename + "does not exist.")
            sys.exit()

    def check_file_exists(self, filename):
        try:
            with open(filename, 'r') as file:
                pass
        except FileNotFoundError:
            print("Sorry, the file "+ filename + "does not exist.")
            sys.exit()

    def check_files_exist(self, filenames):
        for filename in filenames:
            self.check_file_exists(filename)

    def save_to_file(self, filename, data):
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)
        print("Recording has been saved to "+ filename)

    def load_from_file(self, filename):
        with open(filename, 'r') as content:
            data = json.load(content)
        print("Recording has been loaded from "+ filename)
        return data

            

