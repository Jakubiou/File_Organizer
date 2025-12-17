import customtkinter as ctk
from tkinter import filedialog
from multiprocessing import Process, Value, Manager
import os, datetime

from File_Organizer.src.core.Organizer import organize_files


class App:
    def __init__(self):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("File Organizer")
        self.root.geometry("700x600")

        self.progress = Value("i", 0)
        self.total = Value("i", 1)
        self.log = Manager().list()

        self.build_ui()
        self.root.after(200, self.update_ui)

    def build_ui(self):
        self.entry("Input folder")
        ctk.CTkButton(self.root, text="Vybrat", command=self.pick).pack()

        self.slider = ctk.CTkSlider(self.root, 1, 16, command=self.update_label)
        self.slider.set(4)
        self.slider.pack()
        self.proc_label = ctk.CTkLabel(self.root, text="4")
        self.proc_label.pack()

        self.mode = ctk.StringVar(value="type")
        for text, val in [("Typ", "type"), ("Datum", "date"), ("Velikost", "size")]:
            ctk.CTkRadioButton(self.root, text=text, variable=self.mode, value=val).pack()

        self.date_from = ctk.CTkEntry(self.root, placeholder_text="YYYY-MM-DD")
        self.date_to = ctk.CTkEntry(self.root, placeholder_text="YYYY-MM-DD")
        self.size = ctk.CTkEntry(self.root, placeholder_text="Max MB")

        self.date_from.pack()
        self.date_to.pack()
        self.size.pack()

        self.output = ctk.CTkTextbox(self.root, height=80)
        self.output.insert("0.0", "Images:jpg,png\nDocs:txt,pdf")
        self.output.pack()

        self.log_box = ctk.CTkTextbox(self.root, height=150)
        self.log_box.pack()

        self.bar = ctk.CTkProgressBar(self.root)
        self.bar.pack(pady=10)

        ctk.CTkButton(self.root, text="START", command=self.start).pack()

    def entry(self, text):
        ctk.CTkLabel(self.root, text=text).pack()
        self.input = ctk.CTkEntry(self.root, width=400)
        self.input.pack()

    def pick(self):
        path = filedialog.askdirectory()
        if path:
            self.input.delete(0, "end")
            self.input.insert(0, path)

    def update_label(self, v):
        self.proc_label.configure(text=str(int(v)))

    def parse_output(self):
        result = {}
        for line in self.output.get("0.0", "end").splitlines():
            if ":" in line:
                k, v = line.split(":")
                result[k] = v.split(",")
        return result

    def start(self):
        folder = self.input.get()
        if not os.path.isdir(folder):
            self.log.append("Neplatná složka")
            return

        mode = self.mode.get()
        date_from = date_to = size = None

        try:
            if mode == "date":
                date_from = datetime.datetime.fromisoformat(self.date_from.get())
                date_to = datetime.datetime.fromisoformat(self.date_to.get())
            if mode == "size":
                size = float(self.size.get())
        except:
            self.log.append("Špatný vstup")
            return

        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        self.total.value = len(files)
        self.progress.value = 0
        self.log[:] = []

        Process(
            target=organize_files,
            args=(
                folder,
                self.parse_output(),
                int(self.slider.get()),
                mode,
                date_from,
                date_to,
                size,
                self.progress,
                self.log,
            ),
        ).start()

    def update_ui(self):
        if self.total.value:
            self.bar.set(self.progress.value / self.total.value)

        self.log_box.delete("0.0", "end")
        for l in self.log:
            self.log_box.insert("end", l + "\n")

        self.root.after(200, self.update_ui)

    def run(self):
        self.root.mainloop()