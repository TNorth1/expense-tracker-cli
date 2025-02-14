"""Module for handling user input and validation in expense tracking system"""

from datetime import datetime
from decimal import Decimal, localcontext
import re
import tkinter as tk
from tkinter import filedialog, messagebox


VALID_MONEY_FORMAT = r"^\d+(\.\d{2})?$"
VALID_DATE_FORMAT = "%Y-%m-%d"
VALID_CURRENCIES = {
    "د.ج",
    "P",
    "£",
    "ج.م",
    "Br",
    "₵",
    "KSh",
    "د.م.",
    "₦",
    "R",
    "د.ت",
    "֏",
    "৳",
    "Nu.",
    "¥",
    "元",
    "HK$",
    "₹",
    "Rp",
    "₪",
    "₸",
    "د.ك",
    "RM",
    "ر.ع.",
    "₱",
    "ر.ق",
    "ر.س",
    "S$",
    "₩",
    "₫",
    "฿",
    "₭",
    "៛",
    "€",
    "$",
    "C$",
    "A$",
    "NZ$",
    "CHF",
    "руб",
    "₴",
    "₼",
    "₺",
    "₾",
    "L",
    "₣",
}


def money_value_to_decimal(value: str) -> Decimal:
    """Convert a str monetary value to decimal"""
    with localcontext() as ctx:
        ctx.prec = 28
        ctx.rounding = "ROUND_HALF_UP"
        return Decimal(value).quantize(Decimal("0.01"))


def is_valid_date(date_str: str) -> bool:
    """Validate date string format yyyy-mm-dd"""
    try:
        datetime.strptime(date_str, VALID_DATE_FORMAT)
        return True
    except ValueError:
        return False


def is_valid_monetary_value(value_str: str) -> bool:
    """Validate monetary value format (integer or 2 decimal places)"""
    return re.match(VALID_MONEY_FORMAT, value_str) is not None


def is_valid_currency(currency: str) -> bool:
    """Validate currency symbol"""
    return currency in VALID_CURRENCIES


def prompt_for_max_claimable_amount() -> str:
    """Prompt for maximum daily claimable amount"""
    while True:
        print("Enter maximum daily claim amount")
        print("Format: Whole number or 2 decimals (50 or 50.01) or 'unlimited'")
        max_claimable_amount = input("Amount: ")
        if max_claimable_amount == "unlimited":
            return max_claimable_amount
        if is_valid_monetary_value(max_claimable_amount):
            return max_claimable_amount


def prompt_for_currency() -> str:
    """Prompt for currency"""
    while True:
        print("Enter currency symbol (e.g. £ or $)")
        currency = input("Symbol: ")
        if is_valid_currency(currency):
            return currency


def get_date_for_report() -> str:
    """Prompt for expense date in DD/MM/YYYY format"""
    while True:
        print("Enter expense date")
        print("Format: YYYY-MM-DD (blank for today)")
        date = input("Date: ").strip()
        # If user input is left blank, return today's date
        if not date:
            return datetime.today().strftime(VALID_DATE_FORMAT)
        if is_valid_date(date):
            return date


def prompt_for_expense_cost() -> str:
    """Prompt for expense cost"""
    while True:
        print("Enter cost of expense")
        print("Format: Whole number or 2 decimals (50 or 50.01)")
        expense_cost = input("Cost: ")
        if is_valid_monetary_value(expense_cost):
            return expense_cost


def prompt_for_expense_description() -> str:
    """Prompt for expense description"""
    while True:
        print("Enter expense description")
        description = input("Description: ")
        if not description.strip() == "":
            return description


def get_report_data() -> tuple[str, float, str]:
    """Get expense report data from user input"""
    date = get_date_for_report()
    expense_cost = prompt_for_expense_cost()
    description = prompt_for_expense_description()
    return date, expense_cost, description


def continue_adding_expenses() -> bool:
    """Check if user wants to add another expense entry"""
    while True:
        print("Do you want to add another entry?")
        response = input("[y/n]: ")
        if response.lower() in ["y", "n"]:
            return response == "y"


def prompt_export_dir() -> str | None:
    """Prompt user to select directory for file export"""
    # Init Tkinter root widget
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    default_download_path = filedialog.askdirectory(
        initialdir="~/Downloads", title="Select a Directory"
    )

    if default_download_path:
        return default_download_path
    return None


def prompt_file_overwrite(exported_file_path) -> bool:
    """Ask user for confirmation to overwrite existing file"""
    # Init the Tkinter root widget
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    reply = messagebox.askyesno(
        "File Exists", f"{exported_file_path} already exists. Overwrite?"
    )
    return reply
