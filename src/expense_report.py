import json
from rich.table import Table
import os
from src.user_input import UserInput
import pandas as pd


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
    def save_expense_report(report_df, report_path):
        """Writes to and updates the expense report file with new data"""
        with open(report_path, "w") as report_file:
            report_df.to_json(report_file, indent=4)

    @staticmethod
    def create_new_report(storage_directory, file_name, console):
        """Create a new expense report with columns"""
        file_name_with_ext = f"{file_name}.json"
        path = f"{storage_directory}/{file_name_with_ext}"
        columns = {
            "Date": [],
            "Amount": [],
            "Description": [],
        }
        df_columns = pd.DataFrame(columns)
        ExpenseReport.save_expense_report(df_columns, path)

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
    def add_row_to_report(new_report_row, report_path):
        """Adds a new expense row to an expense report"""
        report_file = ExpenseReport.load_expense_report(report_path)
        report_df = pd.DataFrame(report_file)
        # add row to the report_df
        report_df.loc[len(report_df)] = new_report_row
        # sort report df by date and reset index so expense reports are in order
        report_df = report_df.sort_values(by="Date").reset_index(drop=True)
        ExpenseReport.save_expense_report(report_df, report_path)

    @staticmethod
    def add_new_report_row(report_path):
        """A controller method to add a new row to a specified report"""
        add_another_row = True
        while add_another_row:
            new_report_data = UserInput.get_report_data()
            new_report_row = ExpenseReport.init_new_report_row(new_report_data)
            ExpenseReport.add_row_to_report(new_report_row, report_path)
            add_another_row = UserInput.ask_to_add_another_row()

    @staticmethod
    def df_add_total_row(report_df):
        """
        Add the total amount row to the report df to be displayed.
        This will not be written to the report JSON as it is a dynamic value
        """
        total = report_df['Amount'].sum().round(2)
        total_row = {
            "Date": "",
            "Amount": total,
            "Description": ""
        }
        report_df.loc[len(report_df)] = total_row
        return report_df

    @staticmethod
    def format_report_data(report_df):
        """Formats the report rows to be viewed correctly in the terminal. e.g. 9.0 -> £9"""
        # if value float is a digit e.g. 10.0 value -> £10
        # else value float e.g. 10.01 -> £10.01
        report_df['Amount'] = report_df['Amount'].apply(
            lambda x: f"£{int(x) if x == int(x) else x}")
        return report_df

    @ staticmethod
    def format_total_row(formatted_report_df):
        """Formats the total row, adding a prefix to explain it is the total"""
        total_cell = formatted_report_df['Amount'].iloc[-1]
        formatted_report_df.loc[formatted_report_df.index[-1],
                                'Amount'] = f"Total: {total_cell}"
        return formatted_report_df

    @ staticmethod
    def create_table(report_name):
        """Creates table object and sets the tables title and colours"""
        # #BD93F9 - Dracula Purple     #50FA7B - Dracula green
        table = Table(title=f"Expense Report: {report_name}",
                      header_style="bold #BD93F9", border_style="#50FA7B")
        return table

    @ staticmethod
    def populate_table(table, formatted_report_df):
        """Populates a table object with the contents of the expense report"""
        # Add columns to table
        columns = ["ID", "Date", "Amount", "Description"]
        for column in columns:
            table.add_column(column)

        # Add all row to table except total row
        for index, row in formatted_report_df[:-1].iterrows():
            table.add_row(*[str(index + 1), row['Date'],
                          row['Amount'], row['Description']])
            # Add a line between each row
            table.add_section()
        return table

    def populate_table_with_total(table, formatted_report_df):
        """Populates the bottom column of the table with the total row"""
        # Add extra line after report data rows
        table.add_section()
        total_amount = formatted_report_df['Amount'].iloc[-1]
        table.add_row(*['', '', total_amount])
        return table

    @ staticmethod
    def print_table(table, console):
        "Prints the formatted table"
        console.print(table)

    @ staticmethod
    def display_report(report_path, report_name, console):
        """A controller method that displays a specified report"""
        report_data = ExpenseReport.load_expense_report(report_path)
        if report_data is None:
            raise FileNotFoundError("Error: Report does not exist")

        df = pd.DataFrame(report_data)
        df = df.sort_values(by='Date').reset_index(drop=True)
        df_plus_total = ExpenseReport.df_add_total_row(df)

        formatted_df = ExpenseReport.format_report_data(df_plus_total)
        final_df = ExpenseReport.format_total_row(formatted_df)

        table = ExpenseReport.create_table(report_name)
        populated_table = ExpenseReport.populate_table(table, final_df)
        populated_table_with_total = ExpenseReport.populate_table_with_total(
            populated_table, final_df)

        print()
        console.print(populated_table_with_total)

    @ staticmethod
    def list_reports(storage_directory, console):
        """Lists the reports in a report storage directory"""
        report_names = os.listdir(storage_directory)
        # remove extensions from expense reports
        formatted_report_names = [file.split(".")[0] for file in report_names]

        console.print("\n[#50FA7B]Expense Reports:\n")
        for report in formatted_report_names:
            console.print(f"[bold #BD93F9]- {report}")

    @ staticmethod
    def delete_report(report_path, report_name, console):
        """Delete a specified report"""
        try:
            os.remove(report_path)
            console.print(
                f"\n[bold #BD93F9]Successfully removed report: [#50FA7B]{report_name}")
        except FileNotFoundError:
            print("Error: Report does not exist")
