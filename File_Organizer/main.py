import os
import shutil

INPUT_FOLDER = r"C:\Users\Uzivatel\Documents"
OUTPUT_FOLDER = "images"

for f in os.listdir(INPUT_FOLDER):
    if f.lower().endswith((".jpg", ".png")):
        src = os.path.join(INPUT_FOLDER, f)
        dst = os.path.join(OUTPUT_FOLDER, f)
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        shutil.move(src, dst)
        print(f"Přesunuto: {f}")

print("Hotovo!")
