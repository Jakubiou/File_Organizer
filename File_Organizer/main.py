from lib.ConfigLoader import ConfigLoader
from File_Organizer.src.ConfigValidator import Validator
from File_Organizer.src.core.Organizer import organize_files


if __name__ == "__main__":
    try:
        loader = ConfigLoader()
        raw_config = loader.load_config()

        config = Validator.validate(raw_config)

        input_folder = config["input_folder"]
        num_threads = config["num_threads"]
        output_folders = config["output_folders"]
        use_date_range = config["use_date_range"]
        date_from = config.get("date_from", None)
        date_to = config.get("date_to", None)

        print(f"Start přesunu souborů ze složky: {input_folder}")
        organize_files(input_folder, output_folders, num_threads, use_date_range, date_from, date_to)

    except Exception as e:
        print(f"Chyba při načítání konfigurace nebo spuštění programu: {e}")
    input("\nPress ENTER to exit...")
