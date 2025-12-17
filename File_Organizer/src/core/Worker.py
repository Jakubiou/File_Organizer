from .FileMover import move_file

def worker(file_queue, output_folders, mode,date_from, date_to, max_size,progress, shared_log):
    '''
    Worker function for threading that processes files in the queue.
    :param file_queue: Queue containing file paths to move.
    :param output_folders: Mapping of folder names to allowed extensions.
    :return:
    '''
    while True:
        file_path = file_queue.get()
        if file_path is None:
            break

        msg = move_file(file_path,output_folders,mode,date_from,date_to,max_size)

        with progress.get_lock():
            progress.value += 1

        shared_log.append(msg)

