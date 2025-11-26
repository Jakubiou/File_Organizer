import os
import shutil

def move_images(input_folder, output_folder="images"):
    os.makedirs(output_folder, exist_ok=True)

    for f in os.listdir(input_folder):
        if f.lower().endswith((".jpg", ".png")):
            src = os.path.join(input_folder, f)
            dst = os.path.join(output_folder, f)
            shutil.move(src, dst)
            print(f"Přesunuto: {f}")

    print("Hotovo!")
