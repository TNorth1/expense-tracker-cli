import json
from rich.table import Table
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
    def init_storage_directory():
        """Initialise the storage directory for main"""
        storage_directory = ExpenseReport.get_storage_directory()
        os.makedirs(storage_directory, exist_ok=True)
        return storage_directory

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
    def create_new_report(storage_directory, file_name, console):
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
            "Amount": report_data[1],
            "Description": report_data[2],
        }
        return report_row

    @staticmethod
    def append_row_to_report(new_report_row, report_path):
        """Appends a new row to an expense report"""
        report_file = ExpenseReport.load_expense_report(report_path)
        report_file.append(new_report_row)
        ExpenseReport.save_expense_report(report_file, report_path)

    @staticmethod
    def add_new_report_row(report_path):
        """A controller method to add a new row to a specified report"""
        add_another_row = True
        while add_another_row:
            new_report_data = UserInput.get_report_data()
            new_report_row = ExpenseReport.init_new_report_row(new_report_data)
            ExpenseReport.append_row_to_report(new_report_row, report_path)
            add_another_row = UserInput.ask_to_add_another_row()

    @staticmethod
    def calculate_total(report_data):
        """Calculates the total cost of expenses in an expense report"""
        expense_total = 0
        for row in report_data:
            expense_total += row["Amount"]
        # Return to the nearest 2 decimal places to avoid rounding error
        return round(expense_total, 2)

    @staticmethod
    def create_total_row(expense_total):
        """Create a row for the expense total"""
        expense_total_row = {
            "Date": "",
            "Amount": expense_total,
            "Description": ""
        }
        return expense_total_row

    @staticmethod
    def combine_data_with_total(report_data, expense_total_row):
        """
        Combines report data with totals row. Does not alter the report file,
        it is just for the purposes of displaying the report table
        """
        # Convert expense_totals_row to a list, to allow concatenation with report data list
        return report_data + [expense_total_row]

    @staticmethod
    def format_report_data(report_data_with_total):
        """Formats the report rows to be viewed correctly in the terminal. e.g. 9.0 -> £9"""
        for row in report_data_with_total:
            for key, value in row.items():
                if isinstance(value, (int, float)):
                    # if value float is a digit e.g. 10.0 value -> £10
                    # else value float e.g. 10.01 -> £10.01
                    row[key] = f"£{int(value) if value ==
                                   int(value) else value}"

        formatted_report_data = report_data_with_total
        return formatted_report_data

    @staticmethod
    def format_total_row(formatted_report_data):
        """Formats the totals row, adding a prefix to explain it is the total"""
        expense_total = formatted_report_data[-1]["Amount"]
        formatted_report_data[-1]["Amount"] = f"Total = {expense_total}"

        formatted_data_with_total = formatted_report_data
        return formatted_data_with_total

    @staticmethod
    def create_table(report_name):
        """Creates table object and sets the tables title and colours"""
        # #BD93F9 - Dracula Purple     #50FA7B - Dracula green
        table = Table(title=f"Expense Report: {report_name}",
                      header_style="bold #BD93F9", border_style="#50FA7B")
        return table

    @staticmethod
    def populate_table(table, formatted_data_with_total):
        """Populates the contents of the report into a table object"""
        # Add columns to table
        for column in formatted_data_with_total[0].keys():
            table.add_column(column)

        # Add all row to table except grand total row
        for item in formatted_data_with_total[:-1]:
            table.add_row(*[value for value in item.values()])
            # Add a line between each row
            table.add_section()

        # Add extra line after report rows
        table.add_section()
        # Add the grand total row to the table
        table.add_row(*[value for value in formatted_data_with_total[-1].values()])

        return table

    @staticmethod
    def print_table(table, console):
        "Prints the formatted table"
        console.print(table)

    @staticmethod
    def display_report(report_path, report_name, console):
        """A controller method that displays a specified report"""
        report_data = ExpenseReport.load_expense_report(report_path)
        if report_data is None:
            raise FileNotFoundError("Error: Report does not exist")

        expense_total = ExpenseReport.calculate_total(report_data)
        total_row = ExpenseReport.create_total_row(
            expense_total)
        data_with_totals = ExpenseReport.combine_data_with_total(
            report_data, total_row)

        formatted_data = ExpenseReport.format_report_data(
            data_with_totals)
        formatted_data_with_total = ExpenseReport.format_total_row(formatted_data)

        table = ExpenseReport.create_table(report_name)
        ExpenseReport.populate_table(table, formatted_data_with_total)
        print()
        ExpenseReport.print_table(table, console)

    @staticmethod
    def list_reports(storage_directory, console):
        """Lists the reports in a report storage directory"""
        report_names = os.listdir(storage_directory)
        # remove extensions from expense reports
        formatted_report_names = [file.split(".")[0] for file in report_names]

        console.print("\n[#50FA7B]Expense Reports:\n")
        for report in formatted_report_names:
            console.print(f"[bold #BD93F9]- {report}")

    @staticmethod
    def delete_report(report_path, report_name, console):
        """Delete a specified report"""
        try:
            os.remove(report_path)
            console.print(
                f"\n[bold #BD93F9]Successfully removed report: [#50FA7B]{report_name}")
        except FileNotFoundError:
            print("Error: Report does not exist")
