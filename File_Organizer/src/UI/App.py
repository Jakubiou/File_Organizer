import customtkinter as ctk
from tkinter import filedialog


class App:

    def __init__(self):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("File Organizer UI")
        self.root.geometry("500x200")

        self.build_ui()

    def build_ui(self):
        title = ctk.CTkLabel(self.root, text="File Organizer", font=("Arial", 20))
        title.pack(pady=10)

        self.input_entry = ctk.CTkEntry(self.root, width=300, placeholder_text="Vyber složku...")
        self.input_entry.pack(pady=5)

        browse_btn = ctk.CTkButton(self.root, text="Vybrat složku", command=self.pick_folder)
        browse_btn.pack(pady=5)

    def pick_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.input_entry.delete(0, "end")
            self.input_entry.insert(0, path)

    def run(self):
        self.root.mainloop()