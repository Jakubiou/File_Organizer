import os
import threading
import shutil

lock = threading.Lock()

output_folders = {
    "images": ["jpg", "jpeg", "png", "gif"],
    "docs": ["txt", "pdf", "docx", "xlsx"],
    "compressed_files": ["zip", "rar", "7z"]
}

def move_files(input_folder):
    for f in os.listdir(input_folder):
        ext = f.lower().split(".")[-1]
        src = os.path.join(input_folder, f)
        if not os.path.isfile(src):
            continue

        dest_folder = None
        for folder, extensions in output_folders.items():
            if f in extensions:
                dest_folder = folder
                break

        if dest_folder:
            os.makedirs(dest_folder, exist_ok=True)
            dst = os.path.join(dest_folder, f)

            with lock:
                count = 1
                base_name, extn = os.path.splitext(f)
                while os.path.exists(dst):
                    dst = os.path.join(dest_folder, f"{base_name}_({count}){extn}")
                    count += 1

                shutil.move(src, dst)
                print(f"Přesunuto: {f} → {dest_folder}")

    print("Hotovo!")
