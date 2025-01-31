"""Module for functions called by cli sub-commands"""


import os
import sys
import pandas as pd
from rich.console import Console
from src import config_manager
from src import utils
from src import user_input


def create_new_report(storage_directory: str, filename: str, console: Console) -> None:
    """Create new expense report with columns"""
    filename_with_ext = f"{filename}.json"
    path = f"{storage_directory}/{filename_with_ext}"
    columns = {
        "Date": [],
        "Amount": [],
        "Description": [],
    }
    df_columns = pd.DataFrame(columns)
    utils.save_expense_report(df_columns, path)

    console.print(
        f"\n[bold #50FA7B]Created new report: '{filename}'")


def display_summary(
    report_path: str,
    report_name: str,
    max_claimable_amount: float,
    currency: str,
    console: Console
) -> None:
    """Display summarised expense report grouped by date"""
    formatted_report_df = utils.json_to_formatted_summary_df(
        report_path, max_claimable_amount, currency)

    table = utils.create_table("Summary Report", report_name)
    table = utils.populate_summary_table(
        table, formatted_report_df)
    table = utils.populate_summary_table_totals(
        table, formatted_report_df)
    print()
    console.print(table)


def display_report(report_path: str, report_name: str, currency: str, console: Console) -> None:
    """Display expense report"""
    formatted_df = utils.json_to_formatted_report_df(
        report_path, currency)

    table = utils.create_table("Expense Report", report_name)
    table = utils.populate_report_table(
        table, formatted_df)
    table = utils.populate_report_table_total(
        table, formatted_df)
    print()
    console.print(table)


def add_new_report_entry(report_path: str) -> None:
    """Add a new expense to report and ask user to add another expense"""
    continue_adding_expense = True
    while continue_adding_expense:
        report_data = user_input.get_report_data()
        expense = utils.init_new_expense(report_data)
        utils.add_expense_to_report(expense, report_path)
        continue_adding_expense = user_input.continue_adding_expenses()


def list_reports(storage_directory: str, console: Console) -> None:
    """List reports in reports directory"""
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


def handle_rm_row(row_id: int, report_path: str, console: Console) -> None:
    """Remove expense entry by specified ID"""
    report = utils.load_expense_report(report_path)

    try:
        report = utils.rm_row(row_id, report)
    except KeyError:
        console.print(f"[bold #FF5555]Report ID '{row_id}' does not exist")
        sys.exit(1)

    report_df = pd.DataFrame(report).reset_index(drop=True)
    utils.save_expense_report(report_df, report_path)
    console.print(f"[bold #50FA7B]Deleted Report ID: {row_id}")


def delete_report(report_path: str, report_name: str, console: Console) -> None:
    """Delete a specified report"""
    try:
        os.remove(report_path)
        console.print(
            f"\n[bold #50FA7B]Successfully removed report: '{report_name}'")
    except FileNotFoundError:
        print("Error: Report does not exist")


def export_report_to_xlsx(
    report_name: str,
    report_path: str,
    max_claimable_amount: float,
    currency: str,
    console: Console
) -> None:
    """Export report to Excel spreadsheet"""
    report_df = utils.json_to_formatted_report_df(
        report_path, currency)
    summary_df = utils.json_to_formatted_summary_df(
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

    utils.parse_report_to_xlsx(
        report_df, summary_df, path)
    console.print(f"[bold #50FA7B]Exported Expense Report '{
        report_name}' to {export_dir}")


def set_config_setting(
        config: dict[str, str] | float,
        setting_name: str,
        args_value: str | float,
        console: Console
) -> None:
    """Change a config setting value"""
    config[setting_name] = args_value
    config_manager.save_config(config)
    if setting_name == "max_claimable_amount":
        console.print(f"\n[bold #50FA7B]Max daily claimable amount set to: {
            args_value}"
        )
    elif setting_name == "currency":
        console.print(
            f"\n[bold #50FA7B]Currency set to: '{args_value}'")
