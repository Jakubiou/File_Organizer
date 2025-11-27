import os
import threading
from queue import Queue
from .Worker import worker

def organize_files(input_folder, output_folders, num_threads):
    '''
    Organize files from the input folder into destination folders using multiple threads.
    :param input_folder: Folder containing files to organize.
    :param output_folders: Mapping of folder names to allowed extensions.
    :param num_threads: Number of worker threads to use.
    :return:
    '''
    file_queue = Queue()

    for f in os.listdir(input_folder):
        full_path = os.path.join(input_folder, f)
        if os.path.isfile(full_path):
            file_queue.put(full_path)

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(file_queue, output_folders))
        t.start()
        threads.append(t)

    file_queue.join()

    for _ in threads:
        file_queue.put(None)
    for t in threads:
        t.join()

    print("Hotovo! Soubory byly přesunuty.")
