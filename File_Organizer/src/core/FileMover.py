import os
import datetime

from File_Organizer.src.core.SafeFileMove import safe_move

def move_file(file_path, output_folders, mode, date_from, date_to, max_size):
    '''
    Move a file to its corresponding folder based on file extension.
    :param file_path: The full path to the file to move.
    :param output_folders: Dictionary mapping folder names to allowed extensions.
    :return:
    '''

    if not os.path.exists(file_path):
        return f"[SKIP] Soubor neexistuje: {file_path}"

    if mode == "size":
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if size_mb <= max_size:
            final = safe_move(file_path, f"Below_{max_size}_MB")
            return f"[SIZE MOVE] {file_path} -> {final}"
        else:
            return f"[SKIP] {file_path} větší než {max_size} MB"

    if mode == "date":
        stat = os.stat(file_path)
        created = datetime.datetime.fromtimestamp(stat.st_ctime)
        if date_from <= created <= date_to:
            folder = f"{date_from.date()}_to_{date_to.date()}"
            final = safe_move(file_path, folder)
            return f"[DATE MOVE] {file_path} -> {final}"

    ext = file_path.split(".")[-1].lower()
    for folder, extensions in output_folders.items():
        if ext in extensions:
            final = safe_move(file_path, folder)
            return f"[TYPE MOVE] {file_path} -> {final}"

    return f"[SKIP] {file_path} – neznámý typ"
