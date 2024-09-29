import configparser
import os

class Config:
    def __init__(self, config_file='config.ini'):
        self.config_parser = configparser.ConfigParser()

        # Define opciones de configuración por defecto
        default_options = {
            'APP_NAME': 'CivitAI Catalog Creator',
            'DEFAULT_DOWNLOAD_DIR': './downloads',
            'CUSTOMNOTES_DIR': './custom',
            'PROCESSED_FILE': './processed_ids'
        }

        # Añade la sección de 'default' con opciones por defecto
        self.config_parser['DEFAULT'] = default_options

        # Carga el archivo de configuración si existe
        config_path = os.path.join(os.path.dirname(__file__), config_file)
        if os.path.exists(config_path):
            self.config_parser.read(config_path)
        else:
            print(f"Config file not found.")

    def get_option(self, section, option, fallback=None) -> str:
        # Devuelve la opción con un valor de respaldo si no se encuentra
        return self.config_parser.get(section, option, fallback=fallback)
