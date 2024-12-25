import json
import os


def get_storage_directory():

    config_path = "config.json"
    # TODO make this more universal so it doesn't re write all config...
    # once more settings are added
    default_config_data = {
        "storageDirectory": {
            "directory": "NOT_SET"
        }
    }

    try:
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        # if config file does not exist, create it
        with open(config_path, "w") as config_file:
            json.dump(default_config_data, config_file, indent=4)
        config = default_config_data

    # if the storage directory is not set, make the user set the directory
    if (config["storageDirectory"].get("directory") == "NOT_SET" or
            # Checks that user has not edited the config to directory that doesn't exits
            not os.path.isdir(config["storageDirectory"].get("directory"))):
        while True:
            directory = input("Set the directory to store expense reports: ")
            if os.path.isdir(directory):
                config["storageDirectory"]["directory"] = directory
                with open(config_path, "w") as config_file:
                    json.dump(config, config_file, indent=4)
                break
            else:
                print(
                    "Directory does not exist, please try again or create the directory")

    return config["storageDirectory"]["directory"]
