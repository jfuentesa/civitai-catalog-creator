import re
import json
import os

from typing import List

from Exception.AlreadyProcessedException import AlreadyProcessedException
from Exception.DataStructureException import DataStructureException

from downloaded_data import DownloadedData
from config import Config
from processed_manager import ProcessedManager
from url_validator import ValidatorInterface
from downloader import DownloaderInterface

# Clase principal que gestiona el flujo de la aplicación
class CivitaiDownloader:
    def __init__(self, downloader: DownloaderInterface, validator: ValidatorInterface, processed_manager: ProcessedManager):
        self.downloader = downloader
        self.validator = validator
        self.processed_manager = processed_manager
        self.model_version_index = 0
        self.images_url_base = "https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/"

    def run(self, civitai_url: str) -> DownloadedData:
        config = Config()

        try:
            sanitized_url = self.validator.sanitize(civitai_url)
            if not self.validator.validate(sanitized_url):
                raise ValueError("URL not valid.")

            content = self.downloader.download(sanitized_url)

            data = self.extract_json(content)

            # Debugging
            # with open("debug_data.txt", "w") as f:
            #     f.write(str(data))

            self.validate_data_structure(data)

            model_id = self.extract_id(data)
            name = self.extract_name(data)

            print(f"Processing... {name} ({model_id})")

            if self.processed_manager.already_processed_id(model_id):
                raise AlreadyProcessedException(f"{name} ({model_id})")

            type = self.extract_type(data)
            base_model = self.extract_base_model(data)
            filename = self.extract_filename(data)
            clip_skip = self.extract_clip_skip(data)
            trigger_words = self.extract_trigger_words(data)
            images = self.extract_images(data)

            downloaded_data = DownloadedData(
                name=name,
                id=model_id,
                type=type,
                filename=filename,
                base_model=base_model,
                url=civitai_url,
                clip_skip=clip_skip,
                trigger_words=trigger_words,
                images=images
            )

            # Read custom notes
            custom_notes_file_path = os.path.join(config.get_option('DEFAULT', 'CUSTOMNOTES_DIR'), str(downloaded_data.id) + ".html")
            if os.path.exists(custom_notes_file_path):
                with open(custom_notes_file_path, "r") as f:
                    custom_notes = f.read()
                downloaded_data.custom_notes = custom_notes

        except DataStructureException as e:
            raise DataStructureException(str(e))
        except AlreadyProcessedException as e:
            raise AlreadyProcessedException(str(e))
        except Exception as e:
            raise Exception(f"Error: {str(e)}")

        return downloaded_data

    def extract_json(self, content: str) -> dict:
        # Search for the JSON
        match = re.search(r'<script id="__NEXT_DATA__" type="application\/json">\s*(\{.*?\})\s*<\/script>', content, re.S)
        
        if match:
            json_data = json.loads(match.group(1))
            if isinstance(json_data, dict):
                return json_data
            else:
                raise ValueError("El JSON no es correcto.")
        return {}

    def search_value(self, array: dict, search_value, path: str = '') -> str:
        for key, value in array.items():
            current_path = f"{path}->{key}" if path else key

            if isinstance(value, dict):
                result = self.search_value(value, search_value, current_path)
                if result:
                    print(result)
            elif value == search_value:
                print(current_path)
        return None

    def dump_paths(self, content: dict, search_value: str) -> str:
        path = self.search_value(content, search_value)
        return path if path else "No se encontró el valor"

    def extract_id(self, content: dict) -> int:
        # If depends on the presence of modelVersionId in the content
        if "query" in content and "modelVersionId" in content["query"]:
            id = content["query"]["modelVersionId"]
        else:
            id = content["props"]["pageProps"]["trpcState"]["json"]["queries"][5]["state"]["data"]["modelVersions"][0]["id"]
            
        return int(id)

    def extract_name(self, content: dict) -> str:
        model_name = content["props"]["pageProps"]["trpcState"]["json"]["queries"][5]["state"]["data"]["name"]
        model_version = "Unknown"
        loaded_id = self.extract_id(content)

        for index, version in enumerate(content["props"]["pageProps"]["trpcState"]["json"]["queries"][5]["state"]["data"]["modelVersions"]):

            if version["id"] == loaded_id:
                model_version = version["name"]
                self.model_version_index = index

        return f"{model_name} - version: {model_version}"

    def extract_type(self, content: dict) -> str:
        return content["props"]["pageProps"]["trpcState"]["json"]["queries"][5]["state"]["data"]["type"]

    def extract_filename(self, content: dict) -> str:
        return content["props"]["pageProps"]["trpcState"]["json"]["queries"][5]["state"]["data"]["modelVersions"][self.model_version_index]["files"][0]["name"]

    def extract_base_model(self, content: dict) -> str:
        return content["props"]["pageProps"]["trpcState"]["json"]["queries"][5]["state"]["data"]["modelVersions"][self.model_version_index]["baseModel"]

    def extract_clip_skip(self, content: dict) -> int:
        clip_skip = content["props"]["pageProps"]["trpcState"]["json"]["queries"][5]["state"]["data"]["modelVersions"][self.model_version_index]["clipSkip"]
        return int(clip_skip) if isinstance(clip_skip, int) else 0

    def extract_trigger_words(self, content: dict) -> List[str]:
        return content["props"]["pageProps"]["trpcState"]["json"]["queries"][5]["state"]["data"]["modelVersions"][self.model_version_index]["trainedWords"]

    def extract_images(self, content: dict) -> List[str]:
        images = []
        for item in content["props"]["pageProps"]["trpcState"]["json"]["queries"][0]["state"]["data"]["pages"][0]["items"]:
            images.append(f"{self.images_url_base}{item['url']}/width=450/{item['name']}")
        return images

    def validate_data_structure(self, data: dict):
        if "props" not in data or "pageProps" not in data["props"]:
            raise DataStructureException("Missing required data structure in input array")
