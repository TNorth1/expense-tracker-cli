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
        Returns None if the file does not exist
        """
        try:
            with open(Config.CONFIG_PATH, "r") as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            return None

    @staticmethod
    def save_config(config_data):
        """Writes to and updates the config.json file with new config data"""
        with open(Config.CONFIG_PATH, "w") as config_file:
            json.dump(config_data, config_file, indent=4)

    @staticmethod
    def is_valid_config_keys(config):
        """Checks if all of the keys in config.json are correct and untampered with.
        returns True if valid
        """
        config_keys = ["report_storage_directory", "max_claimable_amount"]

        for key in config_keys:
            if key not in config:
                return False
        return True

    @staticmethod
    def set_default_config_settings():
        """Sets the config.json file to default settings"""
        config = Config.DEFAULT_CONFIG_SETTINGS
        Config.save_config(config)

    @staticmethod
    def prompt_for_directory():
        """
        Prompt the user to input a valid directory path.
        Returns the Directory if it is valid
        """
        while True:
            directory = input("Set the directory to store expense reports: ")
            if os.path.isdir(directory):
                return directory
            print("Directory does not exist, please try again or create the directory")

    @staticmethod
    def is_valid_config_directory(config):
        """Returns true if the report_storage_directory setting is valid"""
        return os.path.isdir(config["report_storage_directory"])

    @staticmethod
    def set_storage_directory(config):
        """Sets the storage directory in config.json"""
        config["report_storage_directory"] = Config.prompt_for_directory()
        Config.save_config(config)

    @staticmethod
    def get_storage_directory(config):
        """Returns the storage directory path for expense reports"""
        return config["report_storage_directory"]

    @staticmethod
    def get_max_claimable_amount(config):
        """Returns the daily maximum amount allowed to be claimed in the expense report"""
        return config["max_claimable_amount"]

    @staticmethod
    def set_max_claimable_amount(config):
        """Set the daily maximum amount allowed to be claimed in the expense report"""
        if ARGS.set_max_claimable_amount:
            config["max_claimable_amount"] = ARGS.set_max_claimable_amount
        # else if max_claimable_amount is an invalid value due to file tampering
        else:
            config["max_claimable_amount"] = UserInput.prompt_for_max_claimable_amount()

        Config.save_config(config)


class ExpenseReport:

    @staticmethod
    def load_expense_report(report_path):
        """
        Loads the expense report.
        Returns the report if the file exists.
        Returns None if the file does not exist
        """
        try:
            with open(report_path, "r") as expense_report:
                return json.load(expense_report)
        except FileNotFoundError:
            return None

    @staticmethod
    def save_expense_report(report_data, report_path):
        """Writes to and updates the expense report file with new data"""
        with open(report_path, "w") as report_file:
            json.dump(report_data, report_file, indent=4)

    @staticmethod
    def create_new_report(storage_directory, file_name):
        """Create a new expense report with headers"""
        file_name_with_ext = f"{file_name}.json"
        path = f"{storage_directory}/{file_name_with_ext}"
        empty_array = []

        ExpenseReport.save_expense_report(empty_array, path)

        print(
            f"Created new report '{file_name}' in '{storage_directory}' directory")

    @staticmethod
    def init_new_report_row(report_data):
        """Initialises a new report row"""

        report_row = {
            "Date": report_data[0],
            "Breakfast": report_data[1],
            "Lunch": report_data[2],
            "Dinner": report_data[3],
            "Total": report_data[4],
            "Claimable Total": report_data[5]
        }

        return report_row

    @staticmethod
    def append_row_to_report(new_report_row, report_path):
        """Appends a new row to an expense report"""
        report_file = ExpenseReport.load_expense_report(report_path)
        report_file.append(new_report_row)
        ExpenseReport.save_expense_report(report_file, report_path)


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
    def get_date_for_report():
        """
        Prompts the user for the date of an expense entry and formats it to DD/MM/YYYY
        """
        while True:
            date = input(
                "Enter the date of the expense DD/MM/YYYY (Leave blank to select today's date): ").strip()
            # If user input is left blank, use today's date
            if not date:
                date = datetime.today().strftime('%d/%m/%Y')
                break
            if UserInput.is_valid_date(date):
                break
            print("Enter a valid date - DD/MM/YYYY")

        return date

    @staticmethod
    def get_report_data(max_claimable_amount):
        """Get the expense report data from user input"""
        date = UserInput.get_date_for_report()
        breakfast_cost = UserInput.prompt_for_meal_cost("breakfast")
        lunch_cost = UserInput.prompt_for_meal_cost("lunch")
        dinner_cost = UserInput.prompt_for_meal_cost("dinner")
        # Use round to eliminate floating point error
        total = round(breakfast_cost + lunch_cost + dinner_cost, 2)
        claimable_total = min(total, max_claimable_amount)

        return date, breakfast_cost, lunch_cost, dinner_cost, total, claimable_total
