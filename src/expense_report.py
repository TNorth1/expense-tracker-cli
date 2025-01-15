import json
from rich.table import Table
from rich.console import Console


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

    @staticmethod
    def calculate_grand_total_row(report_data):
        """Calculates the grand total of expenses in a expense report"""

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
    def populate_table(report_name, formatted_report_data):
        # TODO add a create/init table method that splits this down
        # Make this more reusable by making adding the total row
        # a separate function
        """Display the contents of the report in the terminal"""
        table = Table(title=report_name,
                      header_style="bold magenta", border_style="bold green")

        for column in formatted_report_data[0].keys():
            table.add_column(column)

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
