"""Module for functions called by cli sub-commands"""


import os
import sys
import pandas as pd
from src.config_manager import Config
from src import expense_report
from src import user_input


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
    expense_report.save_expense_report(df_columns, path)

    console.print(
        f"\n[bold #50FA7B]Created new report: '{file_name}'")


def display_summary(report_path, report_name, max_claimable_amount, currency, console):
    """A controller method that displays the summarised expense report, grouped by date"""
    formatted_report_df = expense_report.json_to_formatted_summary_df(
        report_path, max_claimable_amount, currency)

    table1 = expense_report.create_table("Summary Report", report_name)
    table2 = expense_report.populate_summary_table(
        table1, formatted_report_df)
    table3 = expense_report.populate_summary_table_totals(
        table2, formatted_report_df)
    print()
    console.print(table3)


def display_report(report_path, report_name, currency, console):
    """A controller method that displays a specified report"""
    formatted_df = expense_report.json_to_formatted_report_df(
        report_path, currency)

    table = expense_report.create_table("Expense Report", report_name)
    populated_table = expense_report.populate_report_table(
        table, formatted_df)
    populated_table_with_total = expense_report.populate_report_table_total(
        populated_table, formatted_df)
    print()
    console.print(populated_table_with_total)


def add_new_report_row(report_path):
    """A controller method to add a new row to a specified report"""
    continue_adding_expense = True
    while continue_adding_expense:
        report_data = user_input.get_report_data()
        expense = expense_report.init_new_expense(report_data)
        expense_report.add_expense_to_report(expense, report_path)
        continue_adding_expense = user_input.continue_adding_expenses()


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


def handle_rm_row(row_id, report_path, console):
    """Handler method for rm --id command"""
    report = expense_report.load_expense_report(report_path)

    try:
        report = expense_report.rm_row(row_id, report)
    except KeyError:
        console.print(f"[bold #FF5555]Report ID '{row_id}' does not exist")
        sys.exit(1)

    report_df = pd.DataFrame(report).reset_index(drop=True)
    expense_report.save_expense_report(report_df, report_path)
    console.print(f"[bold #50FA7B]Deleted Report ID: {row_id}")


def delete_report(report_path, report_name, console):
    """Delete a specified report"""
    try:
        os.remove(report_path)
        console.print(
            f"\n[bold #50FA7B]Successfully removed report: '{report_name}'")
    except FileNotFoundError:
        print("Error: Report does not exist")


def handle_export_command(report_name, report_path, max_claimable_amount, currency, console):
    """A handler method to control the logic for exporting the expense report and summary"""
    report_df = expense_report.json_to_formatted_report_df(
        report_path, currency)
    summary_df = expense_report.json_to_formatted_summary_df(
        report_path, max_claimable_amount, currency)

    export_dir = user_input.prompt_export_dir()
    if export_dir is None:
        console.print("[bold #FF5555]No Directory selected")
        sys.exit(1)

    output_file = f"{report_name}.xlsx"
    path = os.path.join(export_dir, output_file)

    if os.path.exists(path):
        overwrite = user_input.prompt_file_overwrite(path)
        if not overwrite:
            sys.exit(1)

    expense_report.export_report_and_summary(
        report_df, summary_df, path)
    console.print(f"[bold #50FA7B]Exported Expense Report '{
        report_name}' to {export_dir}")


def set_config_setting(config, setting_name, args_value):
    """Set the daily maximum amount allowed to be claimed in the expense report"""
    config[setting_name] = args_value
    Config.save_config(config)
