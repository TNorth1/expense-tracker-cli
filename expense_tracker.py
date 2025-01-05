import json
import os
import argparse

parser = argparse.ArgumentParser(description="Expense tracker")
parser.add_argument('-s', '--set-storage-directory', action='store_true',
                    help="Set the directory to store expense reports in")

args = parser.parse_args()


class Config:
    CONFIG_PATH = "config.json"
    DEFAULT_DIRECTORY = "NOT_SET"
    DEFAULT_CONFIG_DATA = {
        "storageDirectory": {
            "directory": "NOT_SET"
        }
    }

    @staticmethod
    def load_config():
        """Loads the config.json file.
        Returns the config data if the file exists.
        Returns None if the file does not exist.
        """
        try:
            with open(Config.CONFIG_PATH, "r") as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            return None

    @staticmethod
    def save_config(config_data):
        """Writes to and updates the config.json file with new config data."""
        with open(Config.CONFIG_PATH, "w") as config_file:
            json.dump(config_data, config_file, indent=4)

    @staticmethod
    def prompt_for_directory():
        """Prompt the user to input a valid directory path.
        Returns the Directory if it is valid.
        """
        while True:
            directory = input("Set the directory to store expense reports: ")
            if os.path.isdir(directory):
                return directory
            else:
                print(
                    "Directory does not exist, please try again or create the directory")

    @staticmethod
    def set_storage_directory():
        """Sets the storage directory if certain conditions are met."""
        # Create config.json with default values, if it doesn't exist
        config = Config.load_config()
        if config is None:
            config = Config.DEFAULT_CONFIG_DATA
            Config.save_config(config)

        # Update storage directory path with users input if conditions are met
        if (config["storageDirectory"].get("directory") == Config.DEFAULT_DIRECTORY or
                not os.path.isdir(config["storageDirectory"].get("directory")) or
                args.set_storage_directory):
            config["storageDirectory"]["directory"] = Config.prompt_for_directory()
            Config.save_config(config)

    @staticmethod
    def get_storage_directory():
        """Returns the storage directory path for expense reports"""
        try:
            with open(Config.CONFIG_PATH, "r") as config_file:
                config = json.load(config_file)
        except FileNotFoundError:
            print("Config file does not exist")
        else:
            return config["storageDirectory"]["directory"]
