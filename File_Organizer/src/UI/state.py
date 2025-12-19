from multiprocessing import Value, Manager

class AppState:
    '''
    Stores shared application state used for communication between GUI and background processes.
    '''
    def __init__(self):
        self.progress = Value('i', 0)
        self.total_files = Value('i', 1)

        self.manager = Manager()
        self.shared_log = self.manager.list()
