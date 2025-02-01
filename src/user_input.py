"""Module for handling user input and validation in expense tracking system"""


from datetime import datetime
import re
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt5.QtCore import QStandardPaths


VALID_MONEY_FORMAT = r'^\d+(\.\d{2})?$'
VALID_DATE_FORMAT = '%Y-%m-%d'
VALID_CURRENCIES = {
    "د.ج", "P", "£", "ج.م", "Br", "₵", "KSh", "د.م.", "₦", "R",
    "د.ت", "֏", "৳", "Nu.", "¥", "元", "HK$", "₹", "Rp", "₪",
    "₸", "د.ك", "RM", "ر.ع.", "₱", "ر.ق", "ر.س", "S$", "₩", "₫",
    "฿", "₭", "៛", "€", "$", "C$", "A$", "NZ$", "CHF", "руб",
    "₴", "₼", "₺", "₾", "L", "₣"
}


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


def prompt_for_max_claimable_amount() -> float:
    """Prompt for maximum daily claimable amount"""
    while True:
        print("Enter maximum daily claim amount")
        print("Format: Whole number or 2 decimals (50 or 50.01) or 'unlimited'")
        max_claimable_amount = input("Amount: ")
        if max_claimable_amount == "unlimited":
            return max_claimable_amount
        if is_valid_monetary_value(max_claimable_amount):
            return float(max_claimable_amount)


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


def prompt_for_expense_cost() -> float:
    """Prompt for expense cost"""
    while True:
        print("Enter cost of expense")
        print("Format: Whole number or 2 decimals (50 or 50.01)")
        expense_cost = input("Cost: ")
        if is_valid_monetary_value(expense_cost):
            return float(expense_cost)


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
            return response == 'y'


def prompt_export_dir() -> str | None:
    """Prompt user to select directory for file export"""
    # Open file explorer gui in downloads directory (platform agnostic)
    default_download_path = QStandardPaths.writableLocation(
        QStandardPaths.DownloadLocation)
    app = QApplication([])  # Create the application object
    export_dir = QFileDialog.getExistingDirectory(
        None, "Select a Directory", default_download_path)

    if export_dir:
        return export_dir
    return None


def prompt_file_overwrite(exported_file_path) -> bool:
    """Ask user for confirmation to overwrite existing file"""
    app = QApplication([])
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Warning)
    msg_box.setWindowTitle("File Exists")
    msg_box.setText(f"{exported_file_path} already exists. Overwrite?")
    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    reply = msg_box.exec_()
    return reply == QMessageBox.Yes
