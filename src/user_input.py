from datetime import datetime
import re
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt5.QtCore import QStandardPaths


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
        """Validate user input for date in the format yyyy-mm-dd"""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_monetary_value(value_str):
        """Checks if a string is a valid monetary value (integer or float with up two decimal places)"""
        return re.match(r'^\d+(\.\d{2})?$', value_str) is not None

    @staticmethod
    def prompt_for_expense_cost():
        """Prompt the user to input the cost of a specified meal and validates input"""
        while True:
            expense_cost = input("Enter the cost of the expense: ")
            if UserInput.is_valid_monetary_value(expense_cost):
                expense_cost = float(expense_cost)
                break
            else:
                print("Enter a valid monetary value i.e. '10' or '10.01' NOT '10.1'")
        return expense_cost

    @staticmethod
    def get_date_for_report():
        """Prompts the user for the date of an expense entry and formats it to Day DD/MM/YYYY."""
        while True:
            date = input(
                "Enter the date of the expense YYYY-MM-DD (Leave blank to select today's date): ").strip()
            # If user input is left blank, use today's date
            if not date:
                date = datetime.today().strftime('%Y-%m-%d')
                break
            if UserInput.is_valid_date(date):
                break
            print("Enter a valid date - YYYY-MM-DD")
        return date

    @staticmethod
    def get_expense_description():
        """Prompts the user for a description of an expense entry, ensuring it is not left blank"""
        while True:
            description = input("Enter a description: ")
            if not description.strip() == "":
                break
            print("Please enter a description")
        return description

    @staticmethod
    def get_report_data():
        """Get the expense report data from user input"""
        date = UserInput.get_date_for_report()
        expense_cost = UserInput.prompt_for_expense_cost()
        description = UserInput.get_expense_description()
        return date, expense_cost, description

    @staticmethod
    def ask_to_add_another_row():
        """Prompts the user to ask if they want to add another row to a report"""
        while True:
            add_another_row = input("Do you want to add another row? y/n: ")
            if add_another_row.lower() in ["y", "n"]:
                break
            print("Please enter 'y' or 'n'")
        return add_another_row == 'y'

    @staticmethod
    def prompt_export_dir():
        """Prompt the user for the directory to export expense report to"""
        # Open file explorer gui in downloads folder (platform agnostic)
        default_download_path = QStandardPaths.writableLocation(
            QStandardPaths.DownloadLocation)
        app = QApplication([])  # Create the application object
        directory = QFileDialog.getExistingDirectory(
            None, "Select a Directory", default_download_path)

        if directory:
            return directory
        # If no folder is selected
        return None

    @staticmethod
    def prompt_to_overwrite(exported_file_path):
        """Prompt the user to ask if they want to over write a file that already exists"""
        app = QApplication([])
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("File Exists")
        msg_box.setText(f"{exported_file_path} already exists. Overwrite?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        reply = msg_box.exec_()
        return reply == QMessageBox.Yes
