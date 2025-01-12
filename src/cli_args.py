import argparse
import os
import re


def is_valid_arg_directory(directory_path):
    """Validates input for '--set-storage-directory' option ensuring argument is a valid directory path"""
    if not os.path.isdir(directory_path):
        raise argparse.ArgumentTypeError(
            f"{directory_path} is not a valid path for a directory")

    return directory_path


def is_valid_expense_report(filename):
    """Validates input for expense report modification cli args, ensuring the specified expense report exists"""
    # TODO get function to use the storage directory set in the config.json file
    # if user enters the report name without the .json extension, append the extension
    if not filename.endswith(".json"):
        filename = filename + ".json"

    if not os.path.exists(filename):
        filename_without_ext = filename.split(".")[0]
        raise argparse.ArgumentTypeError(
            f"The Expense Report '{filename_without_ext}' does not exist")
    elif filename == "config.json":
        raise argparse.ArgumentTypeError(
            "The config file is not an expense report")

    return filename


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
    parser.add_argument('-n', '--add_new_report_row', type=is_valid_expense_report, required=False,
                        help="Add a new row to a specified expense report")
    parser.add_argument('-m', '--set-max-claimable-amount', type=is_valid_arg_amount, required=False,
                        help="Set the daily maximum amount allowed to be claimed")

    return parser.parse_args()


ARGS = parse_arguments()
