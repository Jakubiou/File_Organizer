import customtkinter as ctk
from File_Organizer.src.lib.ui_builder import UIBuild
from File_Organizer.src.UI.handlers import AppHandlers
from File_Organizer.src.UI.state import AppState

class App:
    '''
    Main application class responsible for initializing the GUI,
    connecting UI components with application state and handlers,
    and running the main event loop.
    '''
    def __init__(self):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("File Organizer UI")
        self.root.geometry("750x850")

        self.state = AppState()

        self.ui = UIBuild(self.root)
        self.handlers = AppHandlers(self.ui, self.state)
        self.ui.build(self.handlers)

        self.root.after(200, self.update_ui)

    def update_ui(self):
        '''
        Periodically updates GUI elements based on shared application state.
        :return:
        '''
        if self.state.total_files.value > 0:
            progress = self.state.progress.value / self.state.total_files.value
            self.ui.progress_bar.set(min(progress, 1.0))

        self.ui.log_box.delete("0.0", "end")
        for line in list(self.state.shared_log):
            self.ui.log_box.insert("end", line + "\n")

        self.root.after(200, self.update_ui)

    def run(self):
        '''
        Main loop responsible for running the main event loop.
        :return:
        '''
        self.root.mainloop()
