import os

from Exception.AlreadyProcessedException import AlreadyProcessedException
from Exception.DataStructureException import DataStructureException
from downloader import CurlDownloader
from url_validator import UrlValidator
from filesaver import FileSaver
from config import Config
from processed_manager import ProcessedManager
from civitai_downloader import CivitaiDownloader

if __name__ == "__main__":
    config = Config()

    if len(os.sys.argv) != 3:
        print("Use: " + os.path.basename(__file__) + " <file> <target_directory>")
        print("Description: Process a set of URLs contained in the specified file and save the results to the target directory.")
    else:
        downloader = CurlDownloader()
        validator = UrlValidator()
        processed_file = config.get_option('DEFAULT', 'PROCESSED_FILE')  # Assuming PROCESSED_FILE is a constant defined elsewhere
        processed_manager = ProcessedManager(processed_file)
        downloader = CivitaiDownloader(downloader, validator, processed_manager)

        file_path = os.sys.argv[1]

        download_base_path = str(os.sys.argv[2] or config.get_option('DEFAULT', 'DEFAULT_DOWNLOAD_DIR'))
        app_name = str(config.get_option('DEFAULT', 'APP_NAME'))
        saver = FileSaver(app_name, download_base_path)

        if os.path.exists(file_path):
            urls = [line for line in open(file_path).read().splitlines() if line.strip()]

            try:
                for url in urls:
                    if validator.validate(url):
                        try:
                            if "modelVersionId=" in url:
                                model_version_id = url.split("=")[1]
                                if processed_manager.already_processed_id(model_version_id):
                                    raise AlreadyProcessedException(f"{model_version_id}")
                            
                            data = downloader.run(url)
                            saver.save(data)
                            processed_manager.save_id(data.id)
                        except DataStructureException as e:
                            print("The data downloaded from this URL has an incorrect data structure: " + str(e))
                        except AlreadyProcessedException as e:
                            print("The model has been already processed: " + str(e))
                    else:
                        print("The URL is not valid: " + url)
            except KeyboardInterrupt as e:
                print("Cancelled by user.")
        else:
            print("The file does not exist: " + file_path)
