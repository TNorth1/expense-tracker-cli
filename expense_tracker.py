import json
import os
import argparse
from datetime import datetime
import re

parser = argparse.ArgumentParser(description="Expense tracker")
parser.add_argument('-s', '--set-storage-directory', action='store_true',
                    help="Set the directory to store expense reports in")
parser.add_argument('-c', '--create-new-report', type=str, required=False,
                    help="Create a new expense report with the specified filename")

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


class ExpenseReport:

    @staticmethod
    def create_report():
        """Create a new expense report with headers"""
        storage_directory = Config.get_storage_directory()
        file_name = f"{args.create_new_report}.json"
        path = f"{storage_directory}/{file_name}"

        headers = {
            "Date": [],
            "Breakfast": [],
            "Lunch": [],
            "Dinner": [],
            "Total": [],
            "Claimable Total": []
        }

        with open(path, 'w') as expense_report:
            json.dump(headers, expense_report, indent=4)


class UserInput:

    @staticmethod
    def is_valid_date(date_str):
        """Validate user input for date in the format dd/mm/yyyy"""
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_monetary_value(value_str):
        """Checks if a string is a valid monetary value (integer or float with up two decimal places)"""
        return re.match(r'^\d+(\.\d{2})?$', value_str) is not None

    @staticmethod
    def get_meal_cost(meal):
        """
        Prompt the user to input the cost of a specified meal.
        The input is validated to ensure it is either an integer or a float with exactly 2 decimal places.
        """
        while True:
            meal_cost = input(f"Enter the cost of {meal}: ")
            if UserInput.is_valid_monetary_value(meal_cost):
                meal_cost = float(meal_cost)
                break
            else:
                print("Enter a valid monetary value i.e. '10' or '10.01' NOT '10.1'")

        return meal_cost

    @staticmethod
    def get_report_data():
        """Get the expense report data from user input"""
        while True:
            date = input(
                "Enter the date of the expense DD/MM/YYYY (Leave blank to select today's date): ")
            if UserInput.is_valid_date(date):
                break
            # If user input is left blank, use today's date
            elif date.strip() == "":
                date = datetime.today().strftime('%d/%m/%Y')
                break
            else:
                print("Enter a valid date - DD/MM/YYYY")

        breakfast_cost = UserInput.get_meal_cost("breakfast")
        lunch_cost = UserInput.get_meal_cost("lunch")
        dinner_cost = UserInput.get_meal_cost("dinner")

        total = breakfast_cost + lunch_cost + dinner_cost

        # 30 is a place holder for now. TODO make claimable total a setting in config.json
        if total > 30:
            claimable_total = 30
        else:
            claimable_total = total

        return date, breakfast_cost, lunch_cost, dinner_cost, total, claimable_total
