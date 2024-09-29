import os
from pathlib import Path
import hashlib
import requests
import html

from downloaded_data import DownloadedData

class FileSaver:
    def __init__(self, app_name: str, download_destination: str = None):
        self.app_name = app_name
        self.download_base_path = download_destination

    def sanitize_to_filename(self, str_to_sanitize: str) -> str:
        if not isinstance(str_to_sanitize, str):
            raise TypeError(f"The string to sanitize must be a string: {str_to_sanitize}")

        sanitized_string = str_to_sanitize.strip().lower()

        valid_chars = set('abcdefghijklmnopqrstuvwxyz0123456789_.-')
        sanitized_string = ''.join(c if c in valid_chars else '_' for c in sanitized_string)

        return sanitized_string

    def save(self, downloaded_data: DownloadedData):
        html_dir_name = "html"
        images_dir_name = "images"

        model_html_path = os.path.join(self.download_base_path, html_dir_name, self.sanitize_to_filename(downloaded_data.base_model), self.sanitize_to_filename(downloaded_data.type))
        downloads_images_path = os.path.join(self.download_base_path, images_dir_name, self.sanitize_to_filename(downloaded_data.type), str(downloaded_data.id))

        os.makedirs(model_html_path, exist_ok=True, mode=0o755)
        os.makedirs(downloads_images_path, exist_ok=True, mode=0o755)
                
        model_html_file = os.path.join(model_html_path, f"{downloaded_data.id}.html")
        full_html_file_path = os.path.join(self.download_base_path, f"{self.sanitize_to_filename(downloaded_data.base_model)}_{self.sanitize_to_filename(downloaded_data.type)}.html")

        with open(model_html_file, "w", encoding="utf-8") as html_file:
            # Write model data
            html_file.write("<div style='margin-bottom: 20px;'>\n")
            html_file.write(f"<h2>{downloaded_data.name}</h2>\n")
            html_file.write(f"<p><strong>Type:</strong> {downloaded_data.type}</p>\n")
            html_file.write(f"<p><strong>Base model:</strong> {downloaded_data.base_model}</p>\n")
            html_file.write(f"<p><strong>Filename:</strong> {downloaded_data.filename.replace('.safetensors', '')}</p>\n")
            html_file.write(f"<p><strong>URL:</strong> <a href='{downloaded_data.url}'>{downloaded_data.url}</a></p>\n")

            if downloaded_data.trigger_words:
                html_file.write(f"<p><strong>Trigger Words:</strong> {', '.join(map(str, downloaded_data.trigger_words))}</p>\n")

            if downloaded_data.clip_skip:
                html_file.write(f"<p><strong>Clip Skip:</strong> {downloaded_data.clip_skip}</p>\n")

            # Write links to images
            html_file.write("<p><strong>Images:</strong></p>\n")
            for index, image_url in enumerate(downloaded_data.images):
                image_name = f'img_{hashlib.sha256(image_url.encode()).hexdigest()}.png'
                
                image_path = os.path.join(downloads_images_path, image_name)

                # Download the image if not exists
                if not os.path.exists(image_path):
                    try:
                        image_content = requests.get(image_url).content
                        with open(image_path, 'wb') as f:
                            f.write(image_content)
                    except Exception as e:
                        print(f"An error occurred while downloading the image {image_url}: {e}")

                # Add image to html
                img_src = f"{images_dir_name}/{self.sanitize_to_filename(downloaded_data.type)}/{downloaded_data.id}/{image_name}"

                html_file.write(f"<img src='{img_src}' style='width: 200px; margin-right: 10px;' />\n")

            # Add custom notes
            html_file.write("<div class=\"notes\">\n")
            if downloaded_data.custom_notes:
                html_file.write(html.escape(str(downloaded_data.custom_notes)))
            html_file.write("</div>\n</div>\n")
            html_file.close()

        # Regerates the entire HTML file
        with open(full_html_file_path, "w", encoding="utf-8") as full_html:
            # Write the header
            full_html.write(f"<html><head><title>{self.app_name}</title></head><body style=\"font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif,Apple Color Emoji,Segoe UI Emoji;\">\n")

            # List all files in the models directory
            files_to_dump = [f for f in os.listdir(model_html_path) if f.endswith(".html")]

            # Write all the html files from the model type directory
            for filename in files_to_dump:
                with open(os.path.join(model_html_path, filename), "r", encoding="utf-8") as file:
                    full_html.write(file.read())

            full_html.write("</body></html>")
            full_html.close()

    def get_urls(self) -> list:
        urls = []
        model_html_paths = f"{self.download_base_path}/html"
        for file in os.listdir(model_html_paths):
            if file.endswith(".html"):
                url = os.path.join(self.download_base_path, file)
                urls.append(url)

        return urls
