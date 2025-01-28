import json
import os
from src.user_input import UserInput


class Config:
    DEFAULT_CONFIG_VALUE = "NOT_SET"
    DEFAULT_CONFIG_SETTINGS = {
        "max_claimable_amount": DEFAULT_CONFIG_VALUE,
        "currency": DEFAULT_CONFIG_VALUE
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
    def validate_config_keys(config):
        """Checks if all of the keys in config.json are correct and untampered with.
        If a config key is missing, add it to the config and return the config
        """
        for key in Config.DEFAULT_CONFIG_SETTINGS:
            if key not in config:
                config[key] = Config.DEFAULT_CONFIG_VALUE
        return config

    @staticmethod
    def set_default_config_settings():
        """Sets the config.json file to default settings"""
        config = Config.DEFAULT_CONFIG_SETTINGS
        Config.save_config(config)

    @staticmethod
    def init_config():
        """Initialise configuration settings for use in main"""
        config = Config.load_config()
        if config is None:
            Config.set_default_config_settings()
            config = Config.load_config()
            return config
        # if config exists, ensure all config settings exist and add them
        # to config.json if they do not
        config = Config.validate_config_keys(config)
        return config

    @staticmethod
    def set_config_setting(config, setting_name, args_value):
        """Set the daily maximum amount allowed to be claimed in the expense report"""
        config[setting_name] = args_value
        Config.save_config(config)

    @staticmethod
    def init_max_claimable_amount(config):
        """
        Initialises the daily maximum amount allowed to be claimed in an
        expense report for main
        """
        max_claimable_amount = config["max_claimable_amount"]
        if max_claimable_amount == Config.DEFAULT_CONFIG_VALUE:
            max_claimable_amount = UserInput.prompt_for_max_claimable_amount()
            Config.set_config_setting(
                config, 'max_claimable_amount', max_claimable_amount)
        return max_claimable_amount

    @staticmethod
    def init_currency(config):
        """Initialises the currency symbol to be used in the expense report for main"""
        currency = config['currency']
        if currency == Config.DEFAULT_CONFIG_VALUE:
            currency = UserInput.prompt_for_currency()
            Config.set_config_setting(config, 'currency', currency)
        return currency
