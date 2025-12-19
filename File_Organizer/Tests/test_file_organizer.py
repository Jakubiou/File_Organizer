import unittest
import os
import shutil
import tempfile
from multiprocessing import Value, Manager, Queue

from File_Organizer.src.core.FileMover import move_file
from File_Organizer.src.core.SafeFileMove import safe_move
from File_Organizer.src.core.Worker import worker

class TestSafeMove(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.dest_dir = os.path.join(self.test_dir, "dest")
        self.file_path = os.path.join(self.test_dir, "test.txt")

        with open(self.file_path, "w") as f:
            f.write("test")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_safe_move_creates_folder_and_moves_file(self):
        result = safe_move(self.file_path, self.dest_dir)

        self.assertTrue(os.path.exists(result))
        self.assertFalse(os.path.exists(self.file_path))

class TestMoveFile(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.file_path = os.path.join(self.test_dir, "image.jpg")

        with open(self.file_path, "w") as f:
            f.write("data")

        self.output_folders = {
            "Images": ["jpg", "png"]
        }

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        if os.path.exists("Images"):
            shutil.rmtree("Images")

    def test_move_file_by_type(self):
        msg = move_file(
            self.file_path,
            self.output_folders,
            mode="type",
            date_from=None,
            date_to=None,
            max_size=None
        )

        self.assertIn("[TYPE MOVE]", msg)
        self.assertTrue(os.path.exists(os.path.join("Images", "image.jpg")))

    def test_move_file_not_existing(self):
        msg = move_file(
            "neexistuje.txt",
            self.output_folders,
            "type",
            None,
            None,
            None
        )

        self.assertIn("[SKIP]", msg)

    def test_move_file_by_size(self):
        msg = move_file(
            self.file_path,
            self.output_folders,
            mode="size",
            date_from=None,
            date_to=None,
            max_size=1
        )

        self.assertIn("[SIZE MOVE]", msg)

class TestWorker(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.file_path = os.path.join(self.test_dir, "doc.txt")

        with open(self.file_path, "w") as f:
            f.write("test")

        self.queue = Queue()
        self.queue.put(self.file_path)
        self.queue.put(None)

        self.output_folders = {"Docs": ["txt"]}

        self.progress = Value("i", 0)
        self.manager = Manager()
        self.shared_log = self.manager.list()

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        if os.path.exists("Docs"):
            shutil.rmtree("Docs")

    def test_worker_processes_file(self):
        worker(
            self.queue,
            self.output_folders,
            mode="type",
            date_from=None,
            date_to=None,
            max_size=None,
            progress=self.progress,
            shared_log=self.shared_log
        )

        self.assertEqual(self.progress.value, 1)
        self.assertEqual(len(self.shared_log), 1)
