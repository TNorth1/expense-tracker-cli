from src import cli_args
from src.config_manager import Config
from src.expense_report import ExpenseReport
from src.user_input import UserInput
import os

ARGS = cli_args.parse_arguments()

STORAGE_DIRECTORY = ExpenseReport.get_storage_directory()
# Create the reports directory if it doesn't exist
os.makedirs(STORAGE_DIRECTORY, exist_ok=True)


# Sets report's name, filename and path if a sub-command that interacts
# with a file is used
try:
    REPORT_FILENAME = ARGS.filename
    # Report name = report file name without .json extension
    REPORT_NAME = REPORT_FILENAME.split(".")[0]
    REPORT_PATH = os.path.join(STORAGE_DIRECTORY, REPORT_FILENAME)
except AttributeError:
    pass

config = Config.load_config()
# Create config file with default settings, if it doesn't exist, is empty
# or the config keys have been tampered with and are not valid
if config is None or not Config.is_valid_config_keys(config):
    Config.set_default_config_settings()
    config = Config.load_config()

max_claimable_amount = config["max_claimable_amount"]
if max_claimable_amount == Config.DEFAULT_CONFIG_VALUE:
    max_claimable_amount = UserInput.prompt_for_max_claimable_amount()
    Config.set_max_claimable_amount(config, max_claimable_amount)

if ARGS.command == 'create':
    ExpenseReport.create_new_report(STORAGE_DIRECTORY, REPORT_NAME)

if ARGS.command == 'display':
    ExpenseReport.display_report(REPORT_PATH, REPORT_NAME)

if ARGS.command == 'update':
    ExpenseReport.add_new_report_row(max_claimable_amount, REPORT_PATH)

if ARGS.command == 'set-max':
    Config.set_max_claimable_amount(config, ARGS.max_claimable_amount)