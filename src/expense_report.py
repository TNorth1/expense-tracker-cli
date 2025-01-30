import os
import sys
import json
import pandas as pd
from rich.table import Table
from src import user_input


def get_storage_directory():
    """Return the absolute path of the report storage directory"""
    current_directory = os.path.dirname(os.path.abspath(__file__))
    storage_directory = os.path.join(
        os.path.dirname(current_directory), 'reports')
    return storage_directory


def init_storage_directory():
    """Initialise the storage directory for main"""
    storage_directory = get_storage_directory()
    os.makedirs(storage_directory, exist_ok=True)
    return storage_directory


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


def save_expense_report(report_df, report_path):
    """Writes to and updates the expense report file with new data"""
    with open(report_path, "w") as report_file:
        report_df.to_json(report_file, indent=4)


def init_new_report_row(report_data):
    """Initialises a new report row"""
    report_row = {
        "Date": report_data[0],
        "Amount": report_data[1],
        "Description": report_data[2],
    }
    return report_row


def add_row_to_report(new_report_row, report_path):
    """Adds a new expense row to an expense report"""
    report_file = load_expense_report(report_path)
    report_df = pd.DataFrame(report_file)
    # add row to the report_df
    report_df.loc[len(report_df)] = new_report_row
    # sort report df by date and reset index so expense reports are in order
    report_df = report_df.sort_values(by="Date").reset_index(drop=True)
    save_expense_report(report_df, report_path)


def df_rm_description(report_df):
    """Delete the Description column in the report df for the purpose of creating a summary report"""
    return report_df.drop(columns="Description")


def df_group_by_date(report_df):
    """Group the report df by date for the purpose of creating a summary report"""
    return report_df.groupby("Date").sum().reset_index()


def df_rename_to_total_col(report_df):
    """Rename the Amount column to the total column in the summary report"""
    return report_df.rename(columns={'Amount': 'Total'})


def df_add_claimable_total(report_df, max_claimable_amount):
    """Adds the Claimable Total row in the summary report"""
    report_df['Claimable Total'] = report_df['Amount'].apply(
        lambda x: min(x, max_claimable_amount))
    return report_df


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


def format_currency(value, currency):
    """Format a an integer or float to a monetary value with a currency symbol"""
    # if value float is a digit e.g. 10.0 value -> £10
    # else value float e.g. 10.01 -> £10.01
    return f"{currency}{int(value) if value == int(value) else round(value, 2)}"


def format_report_data(report_df, currency):
    """Formats the report rows to be viewed correctly in the terminal. e.g. 9.0 -> £9"""
    report_df['Amount'] = report_df['Amount'].apply(
        lambda x: format_currency(x, currency))
    return report_df


def format_grand_total_cell(formatted_report_df, column_name, total_type):
    """Formats the total row, adding a prefix to explain it is the total"""
    cell = formatted_report_df[column_name].iloc[-1]
    formatted_report_df.loc[formatted_report_df.index[-1],
                            column_name] = f"{total_type}: {cell}"
    return formatted_report_df


def format_summary_data(summary_df, currency):
    """Formats the report summary rows to be viewed correctly in the terminal e.g 9.0 -> £9"""
    # if value float is a digit e.g. 10.0 value -> £10
    # else value float e.g. 10.01 -> £10.01
    summary_df['Total'] = summary_df['Total'].apply(
        lambda x: format_currency(x, currency))
    summary_df['Claimable Total'] = summary_df['Claimable Total'].apply(
        lambda x: format_currency(x, currency))
    return summary_df


def format_summary_totals_row(formatted_summary_df, column_name):
    """Formats the summary totals row, adding a prefix to explain it is the total/claimable total"""
    cell = formatted_summary_df[column_name].iloc[-1]
    formatted_summary_df.loc[formatted_summary_df.index[-1],
                             column_name] = f"{column_name}: {cell}"
    return formatted_summary_df


def create_table(title_prefix, report_name):
    """Creates table object and sets the tables title and colours"""
    # Dracula Purple - #BD93F9        Dracula green - #50FA7B
    table = Table(title=f"{title_prefix}: {report_name}",
                  header_style="bold #BD93F9", border_style="#50FA7B")
    return table


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


def populate_report_table_with_total(table, formatted_report_df):
    """Populates the bottom column of the table with the total row"""
    # Add extra line after report data rows
    table.add_section()
    total_amount = formatted_report_df['Amount'].iloc[-1]
    table.add_row(*['', '', total_amount], style="bold yellow")
    return table


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


def populate_summary_table_with_totals(table, formatted_report_df):
    """Populates the bottom column of the table with the total row"""
    # Add extra line after report data rows
    table.add_section()
    grand_total = formatted_report_df['Total'].iloc[-1]
    claimable_total = formatted_report_df['Claimable Total'].iloc[-1]
    table.add_row(*['', grand_total, claimable_total], style="bold yellow")
    return table


def json_to_formatted_report_df(report_path, currency):
    """A Controller method to parse JSON report data to a formatted report df"""
    report_data = load_expense_report(report_path)
    if report_data is None:
        raise FileNotFoundError("Error: Report does not exist")

    df = pd.DataFrame(report_data)
    df_sorted = df.sort_values(by='Date').reset_index(drop=True)
    df_plus_total = df_add_total_row(df_sorted)

    formatted_df = format_report_data(
        df_plus_total, currency)
    formatted_df = format_grand_total_cell(
        formatted_df, "Amount", "Total")

    return formatted_df


def json_to_formatted_summary_df(report_path, max_claimable_amount, currency):
    """A Controller method to parse JSON report data to a formatted report summary df"""
    report_data = load_expense_report(report_path)
    if report_data is None:
        raise FileNotFoundError("Error: Report does not exist")

    df = pd.DataFrame(report_data)
    df_minus_descrip = df_rm_description(df)
    df_grouped = df_group_by_date(df_minus_descrip)
    df_plus_claim_tot = df_add_claimable_total(
        df_grouped, max_claimable_amount)
    df_renamed = df_rename_to_total_col(df_plus_claim_tot)
    df_plus_tot_row = add_summary_totals_row(df_renamed)

    formatted_df1 = format_summary_data(
        df_plus_tot_row, currency)
    formatted_df2 = format_grand_total_cell(
        formatted_df1, "Total", "Total")
    final_formatted_df = format_grand_total_cell(
        formatted_df2, "Claimable Total", "Total")

    return final_formatted_df


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


def rm_row(row_id, report_df):
    """Delete a specified row in an expense report, based on the row ID"""
    for item in report_df.values():
        # row_id - 1 for correct indexing
        del item[str(row_id - 1)]
    return report_df
