"""Module for expense report utility functions"""

import os
import json
import pandas as pd
from rich.table import Table
from src import config_manager
from src import user_input


def init_storage_directory() -> str:
    """Initialise storage directory for main"""
    storage_directory = config_manager.AppInfo.report_dir
    os.makedirs(storage_directory, exist_ok=True)
    return storage_directory


def load_expense_report(report_path: str) -> dict[str, str] | None:
    """Load the expense report"""
    try:
        with open(report_path, "r") as expense_report:
            return json.load(expense_report)
    except FileNotFoundError:
        return None


def save_expense_report(report: pd.DataFrame, report_path: str) -> None:
    """Save expense report"""
    with open(report_path, "w") as report_file:
        report.to_json(report_file, indent=4)


def str_to_decimal_df_column(report: pd.DataFrame) -> pd.DataFrame:
    """Convert report 'amount' column type to decimal"""
    report["Amount"] = report["Amount"].apply(user_input.money_value_to_decimal)
    return report


def init_new_expense(expense_data: tuple[str, str, str]) -> dict[str, str]:
    """Initialise a new expense"""
    expense = {
        "Date": expense_data[0],
        "Amount": expense_data[1],
        "Description": expense_data[2],
    }
    return expense


def add_expense_to_report(expense: dict[str, str], report_path: str) -> None:
    """Add new expense to expense report"""
    report = load_expense_report(report_path)
    report_df = pd.DataFrame(report)
    # add row to the report_df
    report_df.loc[len(report_df)] = expense
    # sort report df by date and reset index so expense reports are in order
    report_df = report_df.sort_values(by="Date").reset_index(drop=True)
    save_expense_report(report_df, report_path)


def rm_description(report_df: pd.DataFrame) -> pd.DataFrame:
    """Remove description column from report for summary report"""
    return report_df.drop(columns="Description")


def group_by_date(report_df: pd.DataFrame) -> pd.DataFrame:
    """Group the summary report by date"""
    return report_df.groupby("Date").sum().reset_index()


def rename_amount_to_total(report_df: pd.DataFrame) -> pd.DataFrame:
    """Rename the 'Amount' column to 'Total' in summary report"""
    return report_df.rename(columns={"Amount": "Total"})


def add_claimable_total(
    report_df: pd.DataFrame, max_claimable_amount: str
) -> pd.DataFrame:
    """Add Claimable Total col to summary report"""
    report_df["Claimable Total"] = report_df["Amount"].apply(
        lambda x: (
            x if max_claimable_amount == "unlimited" else min(x, max_claimable_amount)
        )
    )
    return report_df


def add_summary_totals_row(report_df: pd.DataFrame) -> pd.DataFrame:
    """Add row containing grand total and claimable grand total to the summary report"""
    grand_total = report_df["Total"].sum()
    claimable_total = report_df["Claimable Total"].sum()
    totals_row = {"Date": "", "Total": grand_total, "Claimable Total": claimable_total}
    report_df.loc[len(report_df)] = totals_row
    return report_df


def df_add_total_row(report_df: pd.DataFrame) -> pd.DataFrame:
    """Add total amount row to the report"""
    total = report_df["Amount"].sum()
    total_row = {"Date": "", "Amount": total, "Description": ""}
    report_df.loc[len(report_df)] = total_row
    return report_df


def format_currency(value: str, currency: str) -> str:
    """Add prefixed currency symbol to value"""
    return f"{currency}{value}"


def format_report_data(report_df: pd.DataFrame, currency: str) -> pd.DataFrame:
    """Format report rows e.g. 9.00 -> £9.00"""
    report_df["Amount"] = report_df["Amount"].apply(
        lambda x: format_currency(x, currency)
    )
    return report_df


def format_grand_total_cell(
    report_df: pd.DataFrame, col: str, total_type: str
) -> pd.DataFrame:
    """Format total row, adding prefix to total values"""
    cell = report_df[col].iloc[-1]
    report_df.loc[report_df.index[-1], col] = f"{total_type}: {cell}"
    return report_df


def format_summary_data(summary_df: pd.DataFrame, currency: str) -> pd.DataFrame:
    """Format report summary rows e.g 9.00 -> £9.00"""
    summary_df["Total"] = summary_df["Total"].apply(
        lambda x: format_currency(x, currency)
    )
    summary_df["Claimable Total"] = summary_df["Claimable Total"].apply(
        lambda x: format_currency(x, currency)
    )
    return summary_df


def format_summary_totals_cell(summary_df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Format summary's total row, adding prefix to total values"""
    cell = summary_df[col].iloc[-1]
    summary_df.loc[summary_df.index[-1], col] = f"{col}: {cell}"
    return summary_df


def json_to_formatted_report_df(report_path: str, currency: str) -> pd.DataFrame:
    """Parse JSON report data to formatted report df"""
    report_data = load_expense_report(report_path)
    if report_data is None:
        raise FileNotFoundError("Error: Report does not exist")

    df = pd.DataFrame(report_data)
    df = str_to_decimal_df_column(df)
    df_sorted = df.sort_values(by="Date").reset_index(drop=True)
    df_plus_total = df_add_total_row(df_sorted)

    formatted_df = format_report_data(df_plus_total, currency)
    formatted_df = format_grand_total_cell(formatted_df, "Amount", "Total")

    return formatted_df


def json_to_formatted_summary_df(
    report_path: str, max_claimable_amount: str, currency: str
) -> pd.DataFrame:
    """Parse JSON report data to formatted report summary df"""
    report_data = load_expense_report(report_path)
    if report_data is None:
        raise FileNotFoundError("Error: Report does not exist")

    df = pd.DataFrame(report_data)
    df = str_to_decimal_df_column(df)
    df_minus_descrip = rm_description(df)
    df_grouped = group_by_date(df_minus_descrip)
    df_plus_claim_tot = add_claimable_total(df_grouped, max_claimable_amount)
    df_renamed = rename_amount_to_total(df_plus_claim_tot)
    df_plus_tot_row = add_summary_totals_row(df_renamed)

    formatted_df1 = format_summary_data(df_plus_tot_row, currency)
    formatted_df2 = format_grand_total_cell(formatted_df1, "Total", "Total")
    final_formatted_df = format_grand_total_cell(
        formatted_df2, "Claimable Total", "Total"
    )

    return final_formatted_df


class Colours:
    """Colours to be used in table and success/error messages"""

    border = "#005F73"  # Deep teal
    header = "bold #EE9B00"  # Muted coral
    body = "#E9D8A6"  # Soft sand
    total = "bold #CDAE6D"  # Muted gold

    success = "bold green"
    error = "bold red"


def create_table(title_prefix: str, report_name: str) -> Table:
    """Creates table object and sets the colours"""
    table = Table(
        title=f"{title_prefix}: {report_name}",
        header_style=Colours.header,
        border_style=Colours.border,
    )
    return table


def populate_report_table(table: Table, report_df: pd.DataFrame) -> Table:
    """populate table with data from expense report"""
    # Add columns to table
    columns = ["ID", "Date", "Amount", "Description"]
    for col in columns:
        table.add_column(col)

    # Add all rows to table except total row
    for index, row in report_df[:-1].iterrows():
        table.add_row(
            *[str(index + 1), row["Date"], row["Amount"], row["Description"]],
            style=Colours.body,
        )
        # Add a line between each row
        table.add_section()
    return table


def populate_report_table_total(table: Table, report_df: pd.DataFrame) -> Table:
    """Populate table with total row"""
    # Add extra line after report data rows
    table.add_section()
    total_amount = report_df["Amount"].iloc[-1]
    table.add_row(*["", "", total_amount], style=Colours.total)
    return table


def populate_summary_table(table: Table, summary_df: pd.DataFrame) -> Table:
    """Populate table with data from summary report"""
    # Add columns to table
    columns = ["Date", "Total", "Claimable Total"]
    for col in columns:
        table.add_column(col)

    # Add all rows from to table except total row
    lst_data = [
        summary_df["Date"],
        summary_df["Total"].tolist(),
        summary_df["Claimable Total"].tolist(),
    ]
    for i in range(len(summary_df) - 1):
        table.add_row(
            *[str(lst_data[0][i]), lst_data[1][i], lst_data[2][i]],
            style=Colours.body,
        )
        # Add a line between each row
        table.add_section()
    return table


def populate_summary_table_totals(table: Table, summary_df: pd.DataFrame) -> Table:
    """Populate table with the totals row"""
    # Add extra line after report data rows
    table.add_section()
    grand_total = summary_df["Total"].iloc[-1]
    claimable_total = summary_df["Claimable Total"].iloc[-1]
    table.add_row(*["", grand_total, claimable_total], style=Colours.total)
    return table


def parse_report_to_xlsx(
    report_df: pd.DataFrame, summary_df: pd.DataFrame, export_path: str
) -> None:
    """Parse expense and summary report df's into an xlsx file"""
    with pd.ExcelWriter(export_path, engine="xlsxwriter") as writer:
        report_df.to_excel(writer, sheet_name="Expense Report", index=False)
        summary_df.to_excel(writer, sheet_name="Summary Report", index=False)


def rm_row(row_id: int, report_df: pd.DataFrame) -> pd.DataFrame:
    """Delete an expense row from report"""
    for item in report_df.values():
        # row_id - 1 for correct indexing
        del item[str(row_id - 1)]
    return report_df
