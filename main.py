import os
from rich.console import Console
from src import cli_args
from src.config_manager import Config
from src import expense_report


def main():
    args = cli_args.parse_arguments()
    storage_directory = expense_report.init_storage_directory()
    # Sets report's name, filename and path if a sub-command that interacts
    # with a file is used
    try:
        report_filename = args.filename
        # Report name = report file name without .json extension
        report_name = report_filename.split(".")[0]
        report_path = os.path.join(storage_directory, report_filename)
    except AttributeError:
        pass

    config = Config.init_config()
    max_claimable_amount = Config.init_max_claimable_amount(config)
    currency = Config.init_currency(config)
    # to print colourful text
    console = Console()

    if args.command == 'create':
        expense_report.create_new_report(
            storage_directory, report_name, console)
    elif args.command == 'display':
        if args.summary:
            expense_report.display_summary(
                report_path, report_name, max_claimable_amount, currency, console)
        else:
            expense_report.display_report(
                report_path, report_name, currency, console)
    elif args.command == 'update':
        expense_report.add_new_report_row(report_path)
    elif args.command == 'ls':
        expense_report.list_reports(storage_directory, console)
    elif args.command == 'rm':
        if args.id:
            expense_report.handle_rm_row(args.id, report_path, console)
        else:
            expense_report.delete_report(report_path, report_name, console)
    elif args.command == 'set-max':
        Config.set_config_setting(
            config, 'max_claimable_amount', args.max_claimable_amount)
    elif args.command == 'set-currency':
        Config.set_config_setting(config, 'currency', args.currency)
    elif args.command == 'export':
        expense_report.handle_export_command(
            report_name, report_path, max_claimable_amount, currency, console)


if __name__ == "__main__":
    main()
