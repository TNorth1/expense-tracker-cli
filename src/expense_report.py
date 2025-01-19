import json
from rich.table import Table
from rich.console import Console
import os
from src.user_input import UserInput


class ExpenseReport:

    @staticmethod
    def get_storage_directory():
        """Return the absolute path of the report storage directory"""
        current_directory = os.path.dirname(os.path.abspath(__file__))
        storage_directory = os.path.join(
            os.path.dirname(current_directory), 'reports')
        return storage_directory

    @staticmethod
    def get_report_path(storage_directory, report_name):
        """Creates a report path string from the storage directory and the report name"""
        return os.path.join(storage_directory, report_name)

    @staticmethod
    def add_json_ext(report_path):
        """Adds the .json extension to the report_path"""
        return f"{report_path}.json"

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
        console = Console()
        """Create a new expense report with headers"""
        file_name_with_ext = f"{file_name}.json"
        path = f"{storage_directory}/{file_name_with_ext}"
        empty_array = []

        ExpenseReport.save_expense_report(empty_array, path)

        console.print(
            f"\n[bold #BD93F9]Created new report: [#50FA7B]{file_name}")

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

    @staticmethod
    def add_new_report_row(max_claimable_amount, report_path):
        """A controller method to add a new row to a specified report"""
        new_report_data = UserInput.get_report_data(max_claimable_amount)
        new_report_row = ExpenseReport.init_new_report_row(new_report_data)
        ExpenseReport.append_row_to_report(new_report_row, report_path)

    @staticmethod
    def calculate_grand_total(report_data):
        """Calculates the grand total of expenses in an expense report"""

        grand_total = 0
        claimable_grand_total = 0

        for row in report_data:
            grand_total += row["Total"]
            claimable_grand_total += row["Claimable Total"]

        return grand_total, claimable_grand_total

    @staticmethod
    def create_grand_total_row(grand_total_pair):
        """Create a row for the grand total and the claimable grand total"""
        # unpack the grand_total_pair tuple
        grand_total, claimable_grand_total = grand_total_pair

        # the Grand Total replaces the Total
        # The Claimable Grand Total replaces the Claimable Total
        grand_total_row = {
            "Date": "",
            "Breakfast": "",
            "Lunch": "",
            "Dinner": "",
            "Total": grand_total,
            "Claimable Total": claimable_grand_total
        }

        return grand_total_row

    @staticmethod
    def combine_data_with_grand_totals(report_data, grand_total_row):
        """
        Combines report data with a grand totals row. Does not alter the report file,
        it is just for the purposes of displaying the report table
        """
        # Convert grand_total_row to a list, to allow concatenation with report data list
        return report_data + [grand_total_row]

    @staticmethod
    def format_report_data(report_data_with_totals):
        """Formats the report rows to be viewed correctly in the terminal. e.g. 9.0 -> £9"""
        for row in report_data_with_totals:
            for key, value in row.items():
                if isinstance(value, (int, float)):
                    # if value float is a digit e.g. 10.0 value -> £10
                    # else value float e.g. 10.01 -> £10.01
                    row[key] = f"£{int(value) if value ==
                                   int(value) else value}"

        formatted_report_data = report_data_with_totals

        return formatted_report_data

    @staticmethod
    def create_table(report_name):
        """Creates table object and sets the tables name and colours"""
        # #BD93F9 - Dracula Purple     #50FA7B - Dracula green
        table = Table(title=report_name,
                      header_style="bold #BD93F9", border_style="#50FA7B")
        return table

    @staticmethod
    def populate_table(table, formatted_report_data):
        """Populates the contents of the report in the into a table object"""
        # Add columns to table
        for column in formatted_report_data[0].keys():
            table.add_column(column)

        # Add all row to table except grand total row
        for item in formatted_report_data[:-1]:
            table.add_row(*[value for value in item.values()])
            # Add a line between each row
            table.add_section()

        # Add extra line after report rows
        table.add_section()
        # Add the grand total row to the table
        table.add_row(*[value for value in formatted_report_data[-1].values()])

        return table

    @staticmethod
    def print_table(table):
        "Prints the formatted table"
        console = Console()
        console.print(table)

    @staticmethod
    def display_report(report_path, report_name):
        """A controller method that displays a specified report"""
        report_data = ExpenseReport.load_expense_report(report_path)
        if report_data is None:
            raise FileNotFoundError("Error: Report does not exist")

        grand_total_pair = ExpenseReport.calculate_grand_total(report_data)
        grand_total_row = ExpenseReport.create_grand_total_row(
            grand_total_pair)
        report_data_with_totals = ExpenseReport.combine_data_with_grand_totals(
            report_data, grand_total_row)

        formatted_report_data = ExpenseReport.format_report_data(
            report_data_with_totals)

        table = ExpenseReport.create_table(report_name)
        ExpenseReport.populate_table(table, formatted_report_data)
        ExpenseReport.print_table(table)

    @staticmethod
    def list_reports(storage_directory):
        """Lists the reports in a report storage directory"""
        # Uses the rich library to print colourful text
        console = Console()

        report_names = os.listdir(storage_directory)
        # remove extensions from expense reports
        formatted_report_names = [file.split(".")[0] for file in report_names]

        console.print("\n[#50FA7B]Expense Reports:\n")
        for report in formatted_report_names:
            console.print(f"[bold #BD93F9]- {report}")

    @staticmethod
    def delete_report(report_path, report_name):
        """Delete a specified report"""
        console = Console()
        try:
            os.remove(report_path)
            console.print(
                f"\n[bold #BD93F9]Successfully removed report: [#50FA7B]{report_name}")
        except FileNotFoundError:
            print("Error: Report does not exist")
