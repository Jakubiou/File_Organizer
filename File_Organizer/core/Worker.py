from queue import Queue
from .FileMover import move_file

def worker(file_queue: Queue, output_folders):
    while True:
        file_path = file_queue.get()
        if file_path is None:
            break
        move_file(file_path, output_folders)
        file_queue.task_done()
