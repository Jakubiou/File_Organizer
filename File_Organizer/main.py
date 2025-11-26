import json
import os
from core.Organizer import organize_files

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    config = json.load(f)

input_folder = config.get("input_folder")
num_threads = config.get("num_threads", 1)
output_folders = config.get("output_folders", {})

if not input_folder or not os.path.exists(input_folder):
    print(f"Chyba: složka '{input_folder}' neexistuje!")
else:
    print(f"Start přesunu souborů ze složky: {input_folder}")
    organize_files(input_folder, output_folders, num_threads)
