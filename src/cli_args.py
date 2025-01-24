import argparse
import os
import re
from src.expense_report import ExpenseReport as er


def new_expense_report_name(filename):
    """Validates and adds .json extension to filename if it is not present when creating a new report"""
    if not filename.endswith(".json"):
        filename = f"{filename}.json"

    storage_directory = er.get_storage_directory()
    file_path = os.path.join(storage_directory, filename)

    if os.path.exists(file_path):
        filename_without_ext = filename.split(".")[0]
        raise argparse.ArgumentTypeError(
            f"Report: '{filename_without_ext}' already exists")

    return filename


def is_valid_arg_directory(directory_path):
    """Validates input for '--set-storage-directory' option ensuring argument is a valid directory path"""
    if not os.path.isdir(directory_path):
        raise argparse.ArgumentTypeError(
            f"{directory_path} is not a valid path for a directory")

    return directory_path


def is_valid_expense_report(filename):
    """Validates input for expense report subcommand args, ensuring the specified expense report exists"""
    # if user enters the report name without the .json extension, append the extension
    if not filename.endswith(".json"):
        filename = filename + ".json"

    storage_directory = er.get_storage_directory()
    file_path = os.path.join(storage_directory, filename)

    if not os.path.exists(file_path):
        filename_without_ext = filename.split(".")[0]
        raise argparse.ArgumentTypeError(
            f"The Expense Report '{filename_without_ext}' does not exist")

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
    subparser = parser.add_subparsers(dest='command')

    # Subcommand 'create'
    create_parser = subparser.add_parser(
        'create', help="Create a new expense report with the specified filename")
    create_parser.add_argument(
        'filename', type=new_expense_report_name, help="The filename for the new expense report")

    # Subcommand 'update'
    update_parser = subparser.add_parser(
        'update', help="Add a new row to a specified expense report")
    update_parser.add_argument(
        'filename', type=is_valid_expense_report, help="The filename to add expenses to")

    # Subcommand 'display'
    display_parser = subparser.add_parser(
        'display', help="Display a specified expense report")
    display_parser.add_argument(
        'filename', type=is_valid_expense_report, help="The name of the report to be displayed")
    display_parser.add_argument('--summary', '-s', action='store_true',
                                help="Display the summarised report, grouped by date")

    # Subcommand 'ls'
    subparser.add_parser('ls', help="List all expense reports")

    # Subcommand 'rm'
    rm_parser = subparser.add_parser(
        'rm', help="Remove a specified expense report")
    rm_parser.add_argument(
        'filename', type=is_valid_expense_report, help="The name of the report to be deleted")

    # Subcommand 'set-max'
    set_max_parser = subparser.add_parser(
        'set-max', help="Set the daily maximum amount allowed to be claimed")
    set_max_parser.add_argument('max_claimable_amount', type=is_valid_arg_amount,
                                help="the daily maximum amount allowed to be claimed")

    return parser.parse_args()
