import os
from datetime import datetime

class Validator:
    MIN_THREADS = 1
    MAX_THREADS = 16

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

    num_threads = config.get("num_threads", 1)
    if not isinstance(num_threads, int):
        try:
            num_threads = int(num_threads)
        except (ValueError, TypeError):
            raise ValueError(f"'num_threads' must be an integer, got: {num_threads}")
    if num_threads < Validator.MIN_THREADS or num_threads > Validator.MAX_THREADS:
        print(f"Warning: 'num_threads' out of bounds, resetting to 1")
        num_threads = 1
    validated["num_threads"] = num_threads

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
