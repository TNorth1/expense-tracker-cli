"""Module for expense report config"""

import json
import os
from rich.console import Console
from src import user_input
from src import commands


DEFAULT_CONFIG_VALUE = "NOT_SET"
DEFAULT_CONFIG_SETTINGS = {
    "max_claimable_amount": DEFAULT_CONFIG_VALUE,
    "currency": DEFAULT_CONFIG_VALUE,
}


def get_config_path() -> str:
    """Returns .config.json absolute path"""
    current_directory = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(os.path.dirname(current_directory), ".config.json")
    return config_path


def load_config() -> dict[str, str | float] | None:
    """Load config data if the file exists else returns None"""
    try:
        with open(get_config_path(), "r") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        return None


def save_config(config: dict[str, str | float]) -> None:
    """Update .config.json with new config data"""
    with open(get_config_path(), "w") as config_file:
        json.dump(config, config_file, indent=4)


def validate_config_keys(config: dict[str, str | float]) -> dict[str, str | float]:
    """
    Check if all keys in .config.json are valid.
    If a config key is missing, add it to config.
    """
    for key in DEFAULT_CONFIG_SETTINGS:
        if key not in config:
            config[key] = DEFAULT_CONFIG_VALUE
    return config


def set_default_config_settings() -> None:
    """Reset .config.json to default settings"""
    config = DEFAULT_CONFIG_SETTINGS
    save_config(config)


def init_config() -> dict[str, str | float]:
    """Initialise config for use in main"""
    config = load_config()
    if config is None:
        set_default_config_settings()
        config = load_config()
        return config
    # if config exists, ensure all config settings exist and add them
    # to .config.json if they do not
    config = validate_config_keys(config)
    return config


def init_max_claimable_amount(
    config: dict[str, str | float], console: Console
) -> float:
    """Initialise max claimable amount for use in main"""
    max_claimable_amount = config["max_claimable_amount"]
    if max_claimable_amount == DEFAULT_CONFIG_VALUE:
        console.print("\n[bold #FF5555] Max claimable amount is not set\n")
        max_claimable_amount = user_input.prompt_for_max_claimable_amount()
        commands.set_config_setting(
            config, "max_claimable_amount", max_claimable_amount, console
        )
    return max_claimable_amount


def init_currency(config: dict[str, str | float], console: Console) -> str:
    """Initialises currency symbol for use in main"""
    currency = config["currency"]
    if currency == DEFAULT_CONFIG_VALUE:
        console.print("\n[bold #FF5555] The currency symbol is not set\n")
        currency = user_input.prompt_for_currency()
        commands.set_config_setting(config, "currency", currency, console)
    return currency
