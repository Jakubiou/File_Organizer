import os
from multiprocessing import Lock
import shutil
import datetime

lock = Lock()


def move_file(file_path, output_folders, sort_by_date):
    '''
    Move a file to its corresponding folder based on file extension.
    :param file_path: The full path to the file to move.
    :param output_folders: Dictionary mapping folder names to allowed extensions.
    :return:
    '''
    if sort_by_date:
        stat = os.stat(file_path)
        created = datetime.datetime.fromtimestamp(stat.st_ctime)

        date_folder = created.strftime("%Y-%m-%d")

        os.makedirs(date_folder, exist_ok=True)

        base_name = os.path.basename(file_path)
        dest_path = os.path.join(date_folder, base_name)

        with lock:
            count = 1
            name, extn = os.path.splitext(base_name)
            while os.path.exists(dest_path):
                dest_path = os.path.join(date_folder, f"{name}_({count}){extn}")
                count += 1

            shutil.move(file_path, dest_path)
            print(f"[DATE MOVE] {file_path} -> {dest_path}")
        return

    ext = file_path.split(".")[-1].lower()
    dest_folder = None

    for folder, extensions in output_folders.items():
        if ext in extensions:
            dest_folder = folder
            break

    if not dest_folder:
        return

    os.makedirs(dest_folder, exist_ok=True)
    base_name = os.path.basename(file_path)
    dest_path = os.path.join(dest_folder, base_name)

    with lock:
        count = 1
        name, extn = os.path.splitext(base_name)
        while os.path.exists(dest_path):
            dest_path = os.path.join(dest_folder, f"{name}_({count}){extn}")
            count += 1

        shutil.move(file_path, dest_path)
        print(f"MOVE: {file_path} -> {dest_path}")