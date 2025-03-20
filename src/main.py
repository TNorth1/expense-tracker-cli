"""Main module"""

import os
import sys
from rich.console import Console
from src import cli_args
from src import config_manager
from src import utils
from src import commands


def main():
    try:
        console = Console()
        if len(sys.argv) < 2:
            utils.handle_missing_subcommand(console)

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

        config = config_manager.init_config()
        max_claimable_amount = config_manager.init_max_claimable_amount(config, console)
        currency = config_manager.init_currency(config, console)

        command_dict = {
            "create": lambda: commands.create_new_report(
                storage_directory, report_name, console
            ),
            "display": lambda: commands.display_summary(
                report_path, report_name, max_claimable_amount, currency, console
            )
            if args.summary
            else commands.display_report(report_path, report_name, currency, console),
            "update": lambda: commands.add_new_report_entry(report_path),
            "ls": lambda: commands.list_reports(storage_directory, console),
            "rm": lambda: commands.handle_rm_row(args.id, report_path, console)
            if args.id
            else commands.delete_report(report_path, report_name, console),
            "export": lambda: commands.export_report_to_xlsx(
                report_name, report_path, max_claimable_amount, currency, console
            ),
            "set-max": lambda: commands.set_config_setting(
                config, "max_claimable_amount", args.max_claimable_amount, console
            ),
            "set-currency": lambda: commands.set_config_setting(
                config, "currency", args.currency, console
            ),
            "view-config": lambda: commands.view_config(config, console),
        }

        command_dict[args.command]()

    except KeyboardInterrupt:
        print()
        sys.exit()


if __name__ == "__main__":
    main()
