import os
import datetime

from File_Organizer.src.core.SafeFileMove import safe_move


def move_file(file_path, output_folders, use_date_range, date_from, date_to):
    '''
    Move a file to its corresponding folder based on file extension.
    :param file_path: The full path to the file to move.
    :param output_folders: Dictionary mapping folder names to allowed extensions.
    :return:
    '''

    if use_date_range:
        stat = os.stat(file_path)
        created = datetime.datetime.fromtimestamp(stat.st_ctime)

        if date_from <= created <= date_to:
            folder_name = f"{date_from.strftime('%Y-%m-%d')}_to_{date_to.strftime('%Y-%m-%d')}"
            final_path = safe_move(file_path, folder_name)
            return f"[DATE RANGE MOVE] {file_path} -> {final_path}"

    ext = file_path.split(".")[-1].lower()

    dest_folder = None
    for folder, extensions in output_folders.items():
        if ext in extensions:
            dest_folder = folder
            break

    if not dest_folder:
        return f"[SKIPPED] {file_path} (no folder for .{ext})"

    final_path = safe_move(file_path, dest_folder)
    return f"[MOVE] {file_path} -> {final_path}"
