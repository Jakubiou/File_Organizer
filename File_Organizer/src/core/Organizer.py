import os
from multiprocessing import Process, Queue
from .Worker import worker

def organize_files(input_folder, output_folders, num_processes, use_date_range, date_from, date_to, progress, shared_log):
    '''
    Organize files from the input folder into destination folders using multiple processes.
    :param input_folder: Folder containing files to organize.
    :param output_folders: Mapping of folder names to allowed extensions.
    :param num_processes: Number of worker processes to use.
    :return:
    '''
    file_queue = Queue()

    for f in os.listdir(input_folder):
        full_path = os.path.join(input_folder, f)
        if os.path.isfile(full_path):
            file_queue.put(full_path)

    processes = []
    for _ in range(num_processes):
        p = Process(target=worker,args=(file_queue, output_folders, use_date_range,date_from, date_to, progress, shared_log))
        p.start()
        processes.append(p)

    for _ in processes:
        file_queue.put(None)
    for p in processes:
        p.join()

    print("Hotovo! Soubory byly přesunuty.")
