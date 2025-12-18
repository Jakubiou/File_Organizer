import multiprocessing
import sys
import os

if getattr(sys, 'frozen', False):
    basedir = sys._MEIPASS
else:
    basedir = os.path.dirname(os.path.abspath(__file__))

from src.UI.App import App

if __name__ == "__main__":
    multiprocessing.freeze_support()

    app = App()
    app.run()