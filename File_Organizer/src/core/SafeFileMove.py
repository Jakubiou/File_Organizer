import os
import shutil
from multiprocessing import Lock

move_lock = Lock()

def safe_move(file_path: str, dest_folder: str) -> str:

    os.makedirs(dest_folder, exist_ok=True)

    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)

    dest_path = os.path.join(dest_folder, base_name)

    with move_lock:
        count = 1
        while os.path.exists(dest_path):
            dest_path = os.path.join(dest_folder, f"{name}_({count}){ext}")
            count += 1

        shutil.move(file_path, dest_path)

    return dest_path
