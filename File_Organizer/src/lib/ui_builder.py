import customtkinter as ctk

class UIBuild:
    def __init__(self, root):
        self.root = root

    def build(self, handlers):
        ctk.CTkLabel(self.root, text="Input folder:").pack(pady=5)

        self.input_entry = ctk.CTkEntry(self.root, width=420)
        self.input_entry.pack()

        ctk.CTkButton(
            self.root, text="Vybrat složku",
            command=handlers.pick_folder
        ).pack(pady=5)

        ctk.CTkLabel(self.root, text="Počet procesů:").pack()

        frame = ctk.CTkFrame(self.root)
        frame.pack()

        self.proc_slider = ctk.CTkSlider(
            frame, from_=1, to=16, number_of_steps=15,
            command=handlers.update_process_label
        )
        self.proc_slider.set(4)
        self.proc_slider.pack(side="left", padx=5)

        self.proc_num_label = ctk.CTkLabel(frame, text="4")
        self.proc_num_label.pack(side="left", padx=5)

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

        self.date_from = ctk.CTkEntry(self.root, placeholder_text="Od (YYYY-MM-DD)")
        self.date_from.pack(pady=2)

        self.date_to = ctk.CTkEntry(self.root, placeholder_text="Do (YYYY-MM-DD)")
        self.date_to.pack(pady=2)

        self.size_entry = ctk.CTkEntry(
            self.root, placeholder_text="Max velikost v MB"
        )
        self.size_entry.pack(pady=5)

        ctk.CTkLabel(self.root, text="Output složky (Name:ext,ext)").pack(pady=5)

        self.output_text = ctk.CTkTextbox(self.root, height=120, width=520)
        self.output_text.insert(
            "0.0",
            "Images:jpg,jpeg,png,gif\n"
            "Docs:txt,pdf,docx,xlsx\n"
            "Archives:zip,rar,7z"
        )
        self.output_text.pack()

        self.log_box = ctk.CTkTextbox(self.root, height=150, width=650)
        self.log_box.pack()

        self.progress_bar = ctk.CTkProgressBar(self.root, width=550)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        ctk.CTkButton(
            self.root, text="Start",
            command=handlers.start_process
        ).pack(pady=10)
