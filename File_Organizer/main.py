from lib.ConfigLoader import ConfigLoader
from ConfigValidator.Validator import Validator
from core.Organizer import organize_files

try:
    loader = ConfigLoader()
    raw_config = loader.load_config()

    config = Validator.validate(raw_config)

    input_folder = config["input_folder"]
    num_threads = config["num_threads"]
    output_folders = config["output_folders"]

    print(f"Start přesunu souborů ze složky: {input_folder}")
    organize_files(input_folder, output_folders, num_threads)

except Exception as e:
    print(f"Chyba při načítání konfigurace nebo spuštění programu: {e}")
