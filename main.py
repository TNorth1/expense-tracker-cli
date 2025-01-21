import os
from rich.console import Console
from src import cli_args
from src.config_manager import Config
from src.expense_report import ExpenseReport


def main():
    ARGS = cli_args.parse_arguments()
    STORAGE_DIRECTORY = ExpenseReport.init_storage_directory()
    # Sets report's name, filename and path if a sub-command that interacts
    # with a file is used
    try:
        REPORT_FILENAME = ARGS.filename
        # Report name = report file name without .json extension
        REPORT_NAME = REPORT_FILENAME.split(".")[0]
        REPORT_PATH = os.path.join(STORAGE_DIRECTORY, REPORT_FILENAME)
    except AttributeError:
        pass

    config = Config.init_config()
    max_claimable_amount = Config.init_max_claimable_amount(config)
    # to print colourful text
    console = Console()

    if ARGS.command == 'create':
        ExpenseReport.create_new_report(
            STORAGE_DIRECTORY, REPORT_NAME, console)
    elif ARGS.command == 'display':
        ExpenseReport.display_report(REPORT_PATH, REPORT_NAME, console)
    elif ARGS.command == 'update':
        ExpenseReport.add_new_report_row(REPORT_PATH)
    elif ARGS.command == 'ls':
        ExpenseReport.list_reports(STORAGE_DIRECTORY, console)
    elif ARGS.command == 'rm':
        ExpenseReport.delete_report(REPORT_PATH, REPORT_NAME, console)
    elif ARGS.command == 'set-max':
        Config.set_max_claimable_amount(config, ARGS.max_claimable_amount)


if __name__ == "__main__":
    main()
