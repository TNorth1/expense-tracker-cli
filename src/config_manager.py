import json
import os


class Config:
    DEFAULT_CONFIG_VALUE = "NOT_SET"
    DEFAULT_CONFIG_SETTINGS = {
        "max_claimable_amount": DEFAULT_CONFIG_VALUE
    }

    @staticmethod
    def get_config_path():
        """Returns the config.json absolute path"""
        current_directory = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(os.path.dirname(
            current_directory), 'config.json')
        return config_path

    @staticmethod
    def load_config():
        """
        Loads the config.json file.
        Returns the config data if the file exists.
        Returns None if the file does not exist
        """
        try:
            with open(Config.get_config_path(), "r") as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            return None

    @staticmethod
    def save_config(config_data):
        """Writes to and updates the config.json file with new config data"""
        with open(Config.get_config_path(), "w") as config_file:
            json.dump(config_data, config_file, indent=4)

    @staticmethod
    def is_valid_config_keys(config):
        """Checks if all of the keys in config.json are correct and untampered with.
        returns True if valid
        """
        return "max_claimable_amount" in config

    @staticmethod
    def set_default_config_settings():
        """Sets the config.json file to default settings"""
        config = Config.DEFAULT_CONFIG_SETTINGS
        Config.save_config(config)

    @staticmethod
    def get_max_claimable_amount(config):
        """Returns the daily maximum amount allowed to be claimed in the expense report"""
        return config["max_claimable_amount"]

    @staticmethod
    def set_max_claimable_amount(config, args_value):
        """Set the daily maximum amount allowed to be claimed in the expense report"""
        config["max_claimable_amount"] = args_value
        Config.save_config(config)

    # Currently not used, may be implemented later
    # @staticmethod
    # def prompt_for_directory():
    #     """
    #     Prompt the user to input a valid directory path.
    #     Returns the Directory if it is valid
    #     """
    #     while True:
    #         directory = input("Set the directory to store expense reports: ")
    #         if os.path.isdir(directory):
    #             return directory
    #         print("Directory does not exist, please try again or create the directory")

    # Currently not used, may be implemented later
    # @staticmethod
    # def is_valid_config_directory(config):
    #     """Returns true if the report_storage_directory setting is valid"""
    #     return os.path.isdir(config["report_storage_directory"])

    # Currently not used, may be implemented later
    # @staticmethod
    # def set_storage_directory(config):
    #     """Sets the storage directory in config.json"""
    #     config["report_storage_directory"] = Config.prompt_for_directory()
    #     Config.save_config(config)

    # Currently not used, may be implemented later
    # @staticmethod
    # def get_storage_directory(config):
    #     """Returns the storage directory path for expense reports"""
    #     return config["report_storage_directory"]
