import customtkinter as ctk
from tkinter import filedialog
from multiprocessing import Value, Manager, Process
import os
import datetime

from File_Organizer.src.core.Organizer import organize_files


class App:
    def __init__(self):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("File Organizer UI")
        self.root.geometry("750x850")

        self.progress = Value('i', 0)
        self.total_files = Value('i', 1)

        self.manager = Manager()
        self.shared_log = self.manager.list()

        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(self.root, text="Input folder:").pack(pady=5)

        self.input_entry = ctk.CTkEntry(self.root, width=420)
        self.input_entry.pack()

        ctk.CTkButton(
            self.root, text="Vybrat složku", command=self.pick_folder
        ).pack(pady=5)

        ctk.CTkLabel(self.root, text="Počet procesů:").pack()

        frame = ctk.CTkFrame(self.root)
        frame.pack()

        self.proc_slider = ctk.CTkSlider(
            frame, from_=1, to=16, number_of_steps=15,
            command=self.update_process_label
        )
        self.proc_slider.set(4)
        self.proc_slider.pack(side="left", padx=5)

        self.proc_num_label = ctk.CTkLabel(frame, text="4")
        self.proc_num_label.pack(side="left", padx=5)

        ctk.CTkLabel(self.root, text="Způsob organizace:").pack(pady=5)

        self.mode_var = ctk.StringVar(value="type")

        ctk.CTkRadioButton(
            self.root, text="Podle typu souboru",
            variable=self.mode_var, value="type"
        ).pack()

        ctk.CTkRadioButton(
            self.root, text="Podle data",
            variable=self.mode_var, value="date"
        ).pack()

        ctk.CTkRadioButton(
            self.root, text="Podle velikosti souboru",
            variable=self.mode_var, value="size"
        ).pack()

        self.date_from = ctk.CTkEntry(
            self.root, placeholder_text="Od (YYYY-MM-DD)"
        )
        self.date_from.pack(pady=2)

        self.date_to = ctk.CTkEntry(
            self.root, placeholder_text="Do (YYYY-MM-DD)"
        )
        self.date_to.pack(pady=2)

        self.size_entry = ctk.CTkEntry(
            self.root, placeholder_text="Max velikost v MB (např. 10)"
        )
        self.size_entry.pack(pady=5)

        ctk.CTkLabel(
            self.root, text="Output složky (Název:ext,ext):"
        ).pack(pady=5)

        self.output_text = ctk.CTkTextbox(self.root, height=120, width=520)
        self.output_text.insert(
            "0.0",
            "Images:jpg,jpeg,png,gif\n"
            "Docs:txt,pdf,docx,xlsx\n"
            "Archives:zip,rar,7z"
        )
        self.output_text.pack()

        ctk.CTkLabel(self.root, text="Log:").pack(pady=5)

        self.log_box = ctk.CTkTextbox(self.root, height=150, width=650)
        self.log_box.pack()

        self.progress_bar = ctk.CTkProgressBar(self.root, width=550)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        ctk.CTkButton(
            self.root, text="Start", command=self.start_process
        ).pack(pady=10)

        self.root.after(200, self.update_ui)

    def update_process_label(self, value):
        self.proc_num_label.configure(text=str(int(float(value))))

    def pick_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.input_entry.delete(0, "end")
            self.input_entry.insert(0, path)

    def parse_output(self):
        mapping = {}
        lines = self.output_text.get("0.0", "end").strip().split("\n")
        for line in lines:
            if ":" not in line:
                continue
            folder, ext_raw = line.split(":")
            exts = [e.strip().lower() for e in ext_raw.split(",") if e.strip()]
            mapping[folder.strip()] = exts
        return mapping

    def start_process(self):
        input_folder = self.input_entry.get()
        if not input_folder or not os.path.isdir(input_folder):
            self.shared_log.append("Chybná vstupní složka.")
            return

        mode = self.mode_var.get()
        num_proc = int(self.proc_slider.get())
        output_map = self.parse_output()

        date_from = date_to = None
        max_size = None

        if mode == "date":
            try:
                date_from = datetime.datetime.strptime(
                    self.date_from.get(), "%Y-%m-%d"
                )
                date_to = datetime.datetime.strptime(
                    self.date_to.get(), "%Y-%m-%d"
                )
                if date_from > date_to:
                    raise ValueError
            except Exception:
                self.shared_log.append("Neplatné datum (YYYY-MM-DD).")
                return

        if mode == "size":
            try:
                max_size = float(self.size_entry.get())
                if max_size <= 0:
                    raise ValueError
            except Exception:
                self.shared_log.append("Neplatná velikost souboru v MB.")
                return

        files = [
            f for f in os.listdir(input_folder)
            if os.path.isfile(os.path.join(input_folder, f))
        ]

        self.total_files.value = len(files)
        self.progress.value = 0
        self.shared_log[:] = []

        p = Process(
            target=organize_files,
            args=(
                input_folder,
                output_map,
                num_proc,
                mode,
                date_from,
                date_to,
                max_size,
                self.progress,
                self.shared_log,
            )
        )
        p.start()

    def update_ui(self):
        if self.total_files.value > 0:
            progress = self.progress.value / self.total_files.value
            self.progress_bar.set(min(progress, 1.0))

        self.log_box.delete("0.0", "end")
        for line in list(self.shared_log):
            self.log_box.insert("end", line + "\n")

        self.log_box.see("end")  # auto-scroll
        self.root.after(200, self.update_ui)

    def run(self):
        self.root.mainloop()
