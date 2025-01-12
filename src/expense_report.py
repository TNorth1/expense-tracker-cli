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
    def format_report_rows(report_data):
        """Formats the report rows to be viewed correctly in the terminal. e.g. 9.0 -> £9"""
        for row in report_data:
            for key, value in row.items():
                if isinstance(value, (int, float)):
                    # if value float is a digit e.g. 10.0. value -> £10
                    # else value float e.g. 10.01 -> £10.01
                    row[key] = f"£{int(value) if value ==
                                   int(value) else value}"

        formatted_report_row = report_data
        return formatted_report_row

    @staticmethod
    def view_report(report_name, formatted_report_data):
        """Display the contents of the report in the terminal"""
        table = Table(title=report_name,
                      header_style="bold blue", border_style="bold green")

        for column in formatted_report_data[0].keys():
            table.add_column(column)

        for item in formatted_report_data:
            table.add_row(*[str(value) for value in item.values()])

        console = Console()
        console.print(table)
