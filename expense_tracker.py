import json
import os
import argparse
from datetime import datetime
import re


def is_valid_arg_directory(directory_path):
    """Validates input for '--set-storage-directory' option ensuring argument is a valid directory path"""
    if not os.path.isdir(directory_path):
        raise argparse.ArgumentTypeError(
            f"{directory_path} is not a valid path for a directory")
    return directory_path


def is_valid_arg_amount(value):
    """Validates input for '--set-max-claimable-amount' option ensuring argument a monetary value"""
    # if provided argument is not a valid monetary value, raise error
    if re.match(r'^\d+(\.\d{2})?$', value) is None:
        raise argparse.ArgumentTypeError(
            f"{value} is an invalid value. Enter a valid monetary value i.e. '10' or '10.01' NOT '10.1'")
    return float(value)


def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description="Expense tracker")
    parser.add_argument('-s', '--set-storage-directory', type=is_valid_arg_directory, required=False,
                        help="Set the directory to store expense reports in")
    parser.add_argument('-c', '--create-new-report', type=str, required=False,
                        help="Create a new expense report with the specified filename")
    parser.add_argument('-m', '--set-max-claimable-amount', type=is_valid_arg_amount, required=False,
                        help="Set the daily maximum amount allowed to be claimed")
    return parser.parse_args()


ARGS = parse_arguments()


class Config:
    CONFIG_PATH = "config.json"
    DEFAULT_CONFIG_VALUE = "NOT_SET"
    DEFAULT_CONFIG_SETTINGS = {
        "report_storage_directory": DEFAULT_CONFIG_VALUE,
        "max_claimable_amount": DEFAULT_CONFIG_VALUE
    }

    @staticmethod
    def load_config():
        """
        Loads the config.json file.
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
    def set_default_config_settings():
        """Sets the config.json file to default settings"""
        config = Config.DEFAULT_CONFIG_SETTINGS
        Config.save_config(config)

    @staticmethod
    def prompt_for_directory():
        """
        Prompt the user to input a valid directory path.
        Returns the Directory if it is valid.
        """
        while True:
            directory = input("Set the directory to store expense reports: ")
            if os.path.isdir(directory):
                return directory
            print("Directory does not exist, please try again or create the directory")

    @staticmethod
    def set_storage_directory():
        """Sets the storage directory if certain conditions are met."""
        # Create config.json with default settings if it doesn't exist
        config = Config.load_config()  # TODO this is place holder...
        if config is None:  # ... this logic will go in the main loop
            Config.set_default_config_settings()
            config = Config.load_config()  # Load config again after resetting to default

        current_storage_directory = config["report_storage_directory"]
        # Update storage directory path with users input if conditions are met
        # TODO the conditional check is place holder, it will go in the main loop
        if (current_storage_directory == Config.DEFAULT_CONFIG_VALUE or
                not os.path.isdir(current_storage_directory)):
            config["report_storage_directory"] = Config.prompt_for_directory()
            Config.save_config(config)

    @staticmethod
    def get_storage_directory():
        """Returns the storage directory path for expense reports"""
        config = Config.load_config()
        return config["report_storage_directory"]

    @staticmethod
    def get_max_claimable_amount():
        """Returns the daily maximum amount allowed to be claimed in the expense report"""
        config = Config.load_config()
        return config["max_claimable_amount"]

    @staticmethod
    def set_max_claimable_amount():
        """Set the daily maximum amount allowed to be claimed in the expense report"""
        config = Config.load_config()

        if ARGS.set_max_claimable_amount:
            config["max_claimable_amount"] = ARGS.set_max_claimable_amount
        else:
            config["max_claimable_amount"] = UserInput.prompt_for_max_claimable_amount()

        Config.save_config(config)


class ExpenseReport:

    @staticmethod
    def create_report():
        """Create a new expense report with headers"""
        storage_directory = Config.get_storage_directory()
        file_name = f"{ARGS.create_new_report}.json"
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

        print(
            f"Created new report '{ARGS.create_new_report}' in '{storage_directory}' directory")


class UserInput:

    @staticmethod
    def prompt_for_max_claimable_amount():
        """Prompt the user for daily maximum amount allowed to be claimed in the expense report"""
        while True:
            max_claimable_amount = input(
                "Enter the daily maximum amount allowed to be claimed in expense reports: ")
            if UserInput.is_valid_monetary_value(max_claimable_amount):
                return float(max_claimable_amount)
            print("Enter a valid monetary value i.e. '10' or '10.01' NOT '10.1'")

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
    def prompt_for_meal_cost(meal):
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

        breakfast_cost = UserInput.prompt_for_meal_cost("breakfast")
        lunch_cost = UserInput.prompt_for_meal_cost("lunch")
        dinner_cost = UserInput.prompt_for_meal_cost("dinner")

        # Use round to eliminate floating point error
        total = round(breakfast_cost + lunch_cost + dinner_cost, 2)

        max_claimable_total = Config.get_max_claimable_amount()
        if total > max_claimable_total:
            claimable_total = max_claimable_total
        else:
            claimable_total = total

        return date, breakfast_cost, lunch_cost, dinner_cost, total, claimable_total
