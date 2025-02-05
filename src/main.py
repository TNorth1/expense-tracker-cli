"""Main module"""


import os
from rich.console import Console
from src import cli_args
from src import config_manager
from src import utils
from src import commands


def main():
    args = cli_args.parse_arguments()
    storage_directory = utils.init_storage_directory()
    # Sets report's name, filename and path if a sub-command that interacts
    # with a file is used
    try:
        report_filename = args.filename
        # Report name = report file name without .json extension
        report_name = report_filename.split(".")[0]
        report_path = os.path.join(storage_directory, report_filename)
    except AttributeError:
        pass

    console = Console()

    config = config_manager.init_config()
    max_claimable_amount = config_manager.init_max_claimable_amount(
        config, console)
    currency = config_manager.init_currency(config, console)

    if args.command == 'create':
        commands.create_new_report(
            storage_directory, report_name, console)
    elif args.command == 'display':
        if args.summary:
            commands.display_summary(
                report_path, report_name, max_claimable_amount, currency, console)
        else:
            commands.display_report(
                report_path, report_name, currency, console)
    elif args.command == 'update':
        commands.add_new_report_entry(report_path)
    elif args.command == 'ls':
        commands.list_reports(storage_directory, console)
    elif args.command == 'rm':
        if args.id:
            commands.handle_rm_row(args.id, report_path, console)
        else:
            commands.delete_report(report_path, report_name, console)
    elif args.command == 'export':
        commands.export_report_to_xlsx(
            report_name, report_path, max_claimable_amount, currency, console)
    elif args.command == 'set-max':
        commands.set_config_setting(
            config, 'max_claimable_amount', args.max_claimable_amount, console)
    elif args.command == 'set-currency':
        commands.set_config_setting(
            config, 'currency', args.currency, console)
    elif args.command == 'view-config':
        commands.view_config(config)


if __name__ == "__main__":
    main()
