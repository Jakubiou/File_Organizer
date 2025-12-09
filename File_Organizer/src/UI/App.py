import customtkinter as ctk
from tkinter import filedialog
from multiprocessing import Value, Manager, Process
import os

from File_Organizer.src.core.Organizer import organize_files


class App:

    def __init__(self):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("File Organizer UI")
        self.root.geometry("750x600")

        self.progress = Value('i', 0)
        self.total_files = Value('i', 1)

        self.manager = Manager()
        self.shared_log = self.manager.list()

        self.build_ui()

    def build_ui(self):
        self.input_label = ctk.CTkLabel(self.root, text="Input folder:")
        self.input_label.pack(pady=5)

        self.input_entry = ctk.CTkEntry(self.root, width=400)
        self.input_entry.pack()

        self.browse_btn = ctk.CTkButton(
            self.root, text="Vybrat složku", command=self.pick_folder)
        self.browse_btn.pack(pady=5)

        self.proc_label = ctk.CTkLabel(self.root, text="Počet procesů:")
        self.proc_label.pack()

        frame = ctk.CTkFrame(self.root)
        frame.pack()

        self.proc_slider = ctk.CTkSlider(
            frame, from_=1, to=16, number_of_steps=15,
            command=self.update_process_label
        )
        self.proc_slider.set(4)
        self.proc_slider.pack(side="left", padx=5, pady=5)

        self.proc_num_label = ctk.CTkLabel(frame, text="4")
        self.proc_num_label.pack(side="left", padx=5)

        self.use_date_var = ctk.BooleanVar()
        self.date_checkbox = ctk.CTkCheckBox(
            self.root, text="Použít datumové rozmezí",
            variable=self.use_date_var
        )
        self.date_checkbox.pack(pady=5)

        self.date_from = ctk.CTkEntry(self.root, placeholder_text="Od (YYYY-MM-DD)")
        self.date_from.pack()

        self.date_to = ctk.CTkEntry(self.root, placeholder_text="Do (YYYY-MM-DD)")
        self.date_to.pack()

        self.output_label = ctk.CTkLabel(self.root, text="Output složky (Název:ext,ext):")
        self.output_label.pack(pady=5)

        self.output_text = ctk.CTkTextbox(self.root, height=120, width=500)
        self.output_text.insert("0.0",
"""Images:jpg,jpeg,png,gif
Docs:txt,pdf,docx,xlsx
Archives:zip,rar,7z""")
        self.output_text.pack()

        self.log_label = ctk.CTkLabel(self.root, text="Log:")
        self.log_label.pack(pady=5)

        self.log_box = ctk.CTkTextbox(self.root, height=150, width=600)
        self.log_box.pack()

        self.progress_bar = ctk.CTkProgressBar(self.root, width=500)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        self.start_btn = ctk.CTkButton(
            self.root, text="Start", command=self.start_process
        )
        self.start_btn.pack(pady=10)

        self.root.after(200, self.update_ui)

    def update_process_label(self, value):
        self.proc_num_label.configure(text=str(int(float(value))))

    def pick_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.input_entry.delete(0, "end")
            self.input_entry.insert(0, path)

    def parse_output(self):
        lines = self.output_text.get("0.0", "end").strip().split("\n")
        mapping = {}
        for line in lines:
            if ":" not in line:
                continue
            folder, ext_raw = line.split(":")
            exts = [e.strip() for e in ext_raw.split(",")]
            mapping[folder.strip()] = exts
        return mapping

    def run_organizer(self, cfg):
        organize_files(**cfg)

    def start_process(self):
        input_folder = self.input_entry.get()
        num_proc = int(self.proc_slider.get())
        use_date = self.use_date_var.get()

        date_from = self.date_from.get() if use_date else None
        date_to = self.date_to.get() if use_date else None

        output_map = self.parse_output()

        files = [f for f in os.listdir(input_folder)
                 if os.path.isfile(os.path.join(input_folder, f))]
        self.total_files.value = len(files)
        self.progress.value = 0

        config = dict(
            input_folder=input_folder,
            output_folders=output_map,
            num_processes=num_proc,
            use_date_range=use_date,
            date_from=date_from,
            date_to=date_to,
        )

        p = Process(target=self.run_organizer, args=(config,))
        p.start()

    def update_ui(self):
        if self.total_files.value > 0:
            pr = self.progress.value / self.total_files.value
            self.progress_bar.set(pr)

        self.log_box.delete("0.0", "end")
        for line in list(self.shared_log):
            self.log_box.insert("end", line + "\n")

        self.root.after(200, self.update_ui)

    def run(self):
        self.root.mainloop()
