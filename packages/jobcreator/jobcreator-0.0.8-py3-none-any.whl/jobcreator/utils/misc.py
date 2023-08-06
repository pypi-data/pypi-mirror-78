import json


def get_settings(settings_path: str) -> dict:
    """helper function to load settings"""
    if settings_path == "default":
        settings = {}

    else:
        with open(settings_path, "r") as read_file:
            settings = json.load(read_file)

    return settings
