import os
import sys
import json
from rich.table import Table
import pandas as pd
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
            f"\n[bold #50FA7B]Created new report: '{file_name}'")

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
    def df_rm_description(report_df):
        """Delete the Description column in the report df for the purpose of creating a summary report"""
        return report_df.drop(columns="Description")

    @staticmethod
    def df_group_by_date(report_df):
        """Group the report df by date for the purpose of creating a summary report"""
        return report_df.groupby("Date").sum().reset_index()

    @staticmethod
    def df_rename_to_total_col(report_df):
        """Rename the Amount column to the total column in the summary report"""
        return report_df.rename(columns={'Amount': 'Total'})

    @staticmethod
    def df_add_claimable_total(report_df, max_claimable_amount):
        """Adds the Claimable Total row in the summary report"""
        report_df['Claimable Total'] = report_df['Amount'].apply(
            lambda x: min(x, max_claimable_amount))
        return report_df

    @staticmethod
    def add_summary_totals_row(summary_df):
        """
        Adds a row containing the grand total and the claimable grand total
        to the summary report
        """
        grand_total = summary_df['Total'].sum().round(2)
        claimable_total = summary_df['Claimable Total'].sum().round(2)
        totals_row = {
            "Date": "",
            "Total": grand_total,
            "Claimable Total": claimable_total
        }
        summary_df.loc[len(summary_df)] = totals_row
        return summary_df

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
    def format_currency(value, currency):
        """Format a an integer or float to a monetary value with a currency symbol"""
        # if value float is a digit e.g. 10.0 value -> £10
        # else value float e.g. 10.01 -> £10.01
        return f"{currency}{int(value) if value == int(value) else round(value, 2)}"

    @staticmethod
    def format_report_data(report_df, currency):
        """Formats the report rows to be viewed correctly in the terminal. e.g. 9.0 -> £9"""
        report_df['Amount'] = report_df['Amount'].apply(
            lambda x: ExpenseReport.format_currency(x, currency))
        return report_df

    @ staticmethod
    def format_grand_total_cell(formatted_report_df, column_name, total_type):
        """Formats the total row, adding a prefix to explain it is the total"""
        cell = formatted_report_df[column_name].iloc[-1]
        formatted_report_df.loc[formatted_report_df.index[-1],
                                column_name] = f"{total_type}: {cell}"
        return formatted_report_df

    @staticmethod
    def format_summary_data(summary_df, currency):
        """Formats the report summary rows to be viewed correctly in the terminal e.g 9.0 -> £9"""
        # if value float is a digit e.g. 10.0 value -> £10
        # else value float e.g. 10.01 -> £10.01
        summary_df['Total'] = summary_df['Total'].apply(
            lambda x: ExpenseReport.format_currency(x, currency))
        summary_df['Claimable Total'] = summary_df['Claimable Total'].apply(
            lambda x: ExpenseReport.format_currency(x, currency))
        return summary_df

    @ staticmethod
    def format_summary_totals_row(formatted_summary_df, column_name):
        """Formats the summary totals row, adding a prefix to explain it is the total/claimable total"""
        cell = formatted_summary_df[column_name].iloc[-1]
        formatted_summary_df.loc[formatted_summary_df.index[-1],
                                 column_name] = f"{column_name}: {cell}"
        return formatted_summary_df

    @ staticmethod
    def create_table(title_prefix, report_name):
        """Creates table object and sets the tables title and colours"""
        # Dracula Purple - #BD93F9        Dracula green - #50FA7B
        table = Table(title=f"{title_prefix}: {report_name}",
                      header_style="bold #BD93F9", border_style="#50FA7B")
        return table

    @ staticmethod
    def populate_report_table(table, formatted_report_df):
        """Populates a table object with the contents of the expense report"""
        # Add columns to table
        columns = ["ID", "Date", "Amount", "Description"]
        for col in columns:
            table.add_column(col)

        # Add all rows to table except total row
        for index, row in formatted_report_df[:-1].iterrows():
            table.add_row(*[str(index + 1), row['Date'],
                          row['Amount'], row['Description']], style="bold #F859A8")
            # Add a line between each row
            table.add_section()
        return table

    @staticmethod
    def populate_report_table_with_total(table, formatted_report_df):
        """Populates the bottom column of the table with the total row"""
        # Add extra line after report data rows
        table.add_section()
        total_amount = formatted_report_df['Amount'].iloc[-1]
        table.add_row(*['', '', total_amount], style="bold yellow")
        return table

    @staticmethod
    def populate_summary_table(table, df):
        """Populates a table object with the contents of the summary report"""
        # Add columns to table
        columns = ["Date", "Total", "Claimable Total"]
        for col in columns:
            table.add_column(col)

        # Add all rows from to table except total row
        lst_data = [df["Date"], df["Total"].tolist(
        ), df["Claimable Total"].tolist()]
        for i in range(len(df) - 1):
            table.add_row(
                *[str(lst_data[0][i]), lst_data[1][i], lst_data[2][i]], style='bold #F859A8')
            # Add a line between each row
            table.add_section()
        return table

    @staticmethod
    def populate_summary_table_with_totals(table, formatted_report_df):
        """Populates the bottom column of the table with the total row"""
        # Add extra line after report data rows
        table.add_section()
        grand_total = formatted_report_df['Total'].iloc[-1]
        claimable_total = formatted_report_df['Claimable Total'].iloc[-1]
        table.add_row(*['', grand_total, claimable_total], style="bold yellow")
        return table

    @staticmethod
    def json_to_formatted_report_df(report_path, currency):
        """A Controller method to parse JSON report data to a formatted report df"""
        report_data = ExpenseReport.load_expense_report(report_path)
        if report_data is None:
            raise FileNotFoundError("Error: Report does not exist")

        df = pd.DataFrame(report_data)
        df_sorted = df.sort_values(by='Date').reset_index(drop=True)
        df_plus_total = ExpenseReport.df_add_total_row(df_sorted)

        formatted_df = ExpenseReport.format_report_data(df_plus_total, currency)
        formatted_df = ExpenseReport.format_grand_total_cell(
            formatted_df, "Amount", "Total")

        return formatted_df

    @staticmethod
    def json_to_formatted_summary_df(report_path, max_claimable_amount, currency):
        """A Controller method to parse JSON report data to a formatted report summary df"""
        report_data = ExpenseReport.load_expense_report(report_path)
        if report_data is None:
            raise FileNotFoundError("Error: Report does not exist")

        df = pd.DataFrame(report_data)
        df_minus_descrip = ExpenseReport.df_rm_description(df)
        df_grouped = ExpenseReport.df_group_by_date(df_minus_descrip)
        df_plus_claim_tot = ExpenseReport.df_add_claimable_total(
            df_grouped, max_claimable_amount)
        df_renamed = ExpenseReport.df_rename_to_total_col(df_plus_claim_tot)
        df_plus_tot_row = ExpenseReport.add_summary_totals_row(df_renamed)

        formatted_df1 = ExpenseReport.format_summary_data(df_plus_tot_row, currency)
        formatted_df2 = ExpenseReport.format_grand_total_cell(
            formatted_df1, "Total", "Total")
        final_formatted_df = ExpenseReport.format_grand_total_cell(
            formatted_df2, "Claimable Total", "Total")

        return final_formatted_df

    @ staticmethod
    def display_report(report_path, report_name, currency, console):
        """A controller method that displays a specified report"""
        formatted_df = ExpenseReport.json_to_formatted_report_df(report_path, currency)

        table = ExpenseReport.create_table("Expense Report", report_name)
        populated_table = ExpenseReport.populate_report_table(
            table, formatted_df)
        populated_table_with_total = ExpenseReport.populate_report_table_with_total(
            populated_table, formatted_df)
        print()
        console.print(populated_table_with_total)

    @staticmethod
    def display_summary(report_path, report_name, max_claimable_amount, currency, console):
        """A controller method that displays the summarised expense report, grouped by date"""
        formatted_report_df = ExpenseReport.json_to_formatted_summary_df(
            report_path, max_claimable_amount, currency)

        table1 = ExpenseReport.create_table("Summary Report", report_name)
        table2 = ExpenseReport.populate_summary_table(
            table1, formatted_report_df)
        table3 = ExpenseReport.populate_summary_table_with_totals(
            table2, formatted_report_df)
        print()
        console.print(table3)

    @ staticmethod
    def list_reports(storage_directory, console):
        """Lists the reports in a report storage directory"""
        report_names = os.listdir(storage_directory)
        # if the report directory is empty
        if report_names == []:
            console.print("[bold #FF5555]There are no reports to list")
            sys.exit(1)

        # remove extensions from expense reports
        formatted_report_names = [file.split(".")[0] for file in report_names]

        console.print("\n[#50FA7B]Expense Reports:\n")
        for report in formatted_report_names:
            console.print(f"  [bold #BD93F9]- {report}")

    @ staticmethod
    def delete_report(report_path, report_name, console):
        """Delete a specified report"""
        try:
            os.remove(report_path)
            console.print(
                f"\n[bold #50FA7B]Successfully removed report: '{report_name}'")
        except FileNotFoundError:
            print("Error: Report does not exist")

    @staticmethod
    def export_report_and_summary(report_df, summary_df, export_path):
        """
        Export the expense report and the summary report into an excel spreadsheet,
        separated by 2 tabs
        """
        with pd.ExcelWriter(export_path, engine='xlsxwriter') as writer:
            report_df.to_excel(
                writer, sheet_name='Expense Report', index=False)
            summary_df.to_excel(
                writer, sheet_name='Summary Report', index=False)

    @staticmethod
    def handle_export_command(report_name, report_path, max_claimable_amount, currency, console):
        """A handler method to control the logic for exporting the expense report and summary"""
        report_df = ExpenseReport.json_to_formatted_report_df(report_path, currency)
        summary_df = ExpenseReport.json_to_formatted_summary_df(
            report_path, max_claimable_amount, currency)

        export_dir = UserInput.prompt_export_dir()
        if export_dir is None:
            console.print("[bold #FF5555]No Directory selected")
            sys.exit(1)

        output_file = f"{report_name}.xlsx"
        path = os.path.join(export_dir, output_file)

        if os.path.exists(path):
            overwrite = UserInput.prompt_to_overwrite(path)
            if not overwrite:
                sys.exit(1)

        ExpenseReport.export_report_and_summary(
            report_df, summary_df, path)
        console.print(f"[bold #50FA7B]Exported Expense Report '{
                      report_name}' to {export_dir}")

    @staticmethod
    def rm_row(row_id, report_df):
        """Delete a specified row in an expense report, based on the row ID"""
        for item in report_df.values():
            # row_id - 1 for correct indexing
            del item[str(row_id - 1)]
        return report_df

    @staticmethod
    def handle_rm_row(row_id, report_path, console):
        """Handler method for rm --id command"""
        report = ExpenseReport.load_expense_report(report_path)

        try:
            report = ExpenseReport.rm_row(row_id, report)
        except KeyError:
            console.print(f"[bold #FF5555]Report ID '{row_id}' does not exist")
            sys.exit(1)

        report_df = pd.DataFrame(report).reset_index(drop=True)
        ExpenseReport.save_expense_report(report_df, report_path)
        console.print(f"[bold #50FA7B]Deleted Report ID: {row_id}")
