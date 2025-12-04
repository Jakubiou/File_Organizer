import os
from datetime import datetime

class Validator:
    MIN_PROCESSES = 1
    MAX_PROCESSES = 16

@staticmethod
def validate(config):
    '''
     Validate the given configuration dictionary.
    :param: config (dict): The raw configuration dictionary to validate.
    :return: dict: A validated configuration dictionary with correct types and limits applied.
    '''
    validated = {}

    input_folder = config.get("input_folder")
    if not isinstance(input_folder, str) or not os.path.exists(input_folder):
        raise ValueError(f"Invalid 'input_folder': {input_folder}")
    validated["input_folder"] = input_folder

    num_processes = config.get("num_processes", 1)
    if not isinstance(num_processes, int):
        try:
            num_processes = int(num_processes)
        except (ValueError, TypeError):
            raise ValueError(f"'num_processes' must be an integer, got: {num_processes}")
    if num_processes < Validator.MIN_PROCESSES or num_processes > Validator.MAX_PROCESSES:
        print(f"Warning: 'num_processes' out of bounds, resetting to 1")
        num_processes = 1
    validated["num_processes"] = num_processes

    output_folders = config.get("output_folders", {})
    if not isinstance(output_folders, dict):
        raise ValueError("'output_folders' must be a dictionary")

    for folder, extensions in output_folders.items():
        if not isinstance(folder, str):
            raise ValueError(f"Folder name must be a string: {folder}")
        if not isinstance(extensions, list) or not all(isinstance(ext, str) for ext in extensions):
            raise ValueError(f"Extensions for folder '{folder}' must be a list of strings")
    validated["output_folders"] = output_folders

    use_date_range = config.get("use_date_range", False)
    if not isinstance(use_date_range, bool):
        raise ValueError("'use_date_range' must be true/false")
    validated["use_date_range"] = use_date_range

    if use_date_range:
        date_from = config.get("date_from", None)
        date_to = config.get("date_to", None)

        try:
            date_from = datetime.strptime(date_from, "%Y-%m-%d")
            date_to = datetime.strptime(date_to, "%Y-%m-%d")
        except Exception:
            raise ValueError("'date_from' and 'date_to' must be in format YYYY-MM-DD")

        if date_from > date_to:
            raise ValueError("date_from cannot be after date_to")

        validated["date_from"] = date_from
        validated["date_to"] = date_to

    return validated
