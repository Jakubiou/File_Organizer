import os
import datetime
from multiprocessing import Process
from File_Organizer.src.core.Organizer import organize_files
from tkinter import filedialog

class AppHandlers:
    '''
    Handles all user interactions and events triggered from the GUI.
    '''
    def __init__(self, ui, state):
        self.ui = ui
        self.state = state

    def update_process_label(self, value):
        '''
         Updates the label displaying the selected number of processes when the slider value changes.
        :param value: Current slider value
        :return: number  of processes
        '''
        self.ui.proc_num_label.configure(text=str(int(float(value))))

    def pick_folder(self):
        '''
        Picks the folder selected by the user.
        :return:
        '''
        path = filedialog.askdirectory()
        if path:
            self.ui.input_entry.delete(0, "end")
            self.ui.input_entry.insert(0, path)

    def parse_output(self):
        '''
        Parses the output from the GUI.
        :return:
        '''
        mapping = {}
        lines = self.ui.output_text.get("0.0", "end").strip().split("\n")
        for line in lines:
            if ":" not in line:
                continue
            folder, ext_raw = line.split(":")
            mapping[folder.strip()] = [
                e.strip().lower() for e in ext_raw.split(",") if e.strip()
            ]
        return mapping

    def start_process(self):
        '''
        Starts the GUI event loop.
        :return:
        '''
        input_folder = self.ui.input_entry.get()
        if not os.path.isdir(input_folder):
            self.state.shared_log.append("Invalid input folder.")
            return

        mode = self.ui.mode_var.get()
        num_proc = int(self.ui.proc_slider.get())
        output_map = self.parse_output()

        date_from = date_to = max_size = None

        if mode == "date":
            try:
                date_from = datetime.datetime.strptime(
                    self.ui.date_from.get(), "%Y-%m-%d"
                )
                date_to = datetime.datetime.strptime(
                    self.ui.date_to.get(), "%Y-%m-%d"
                )
            except:
                self.state.shared_log.append("Invalid date format.")
                return

        if mode == "size":
            try:
                max_size = float(self.ui.size_entry.get())
            except:
                self.state.shared_log.append("Invalid file size.")
                return

        files = [
            f for f in os.listdir(input_folder)
            if os.path.isfile(os.path.join(input_folder, f))
        ]

        self.state.total_files.value = len(files)
        self.state.progress.value = 0
        self.state.shared_log[:] = []

        Process(
            target=organize_files,
            args=(
                input_folder,
                output_map,
                num_proc,
                mode,
                date_from,
                date_to,
                max_size,
                self.state.progress,
                self.state.shared_log
            )
        ).start()
