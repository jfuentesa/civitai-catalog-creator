import requests

# Interface para el downloader, en línea con el principio de inversión de dependencias (D de SOLID)
class DownloaderInterface:
    def download(self, url):
        raise NotImplementedError("Implementa el método 'download'")

# Implementación del downloader usando requests
class CurlDownloader(DownloaderInterface):
    def download(self, url: str) -> str:
        # Configura las opciones de request
        response = requests.get(url)

        # Manejo de errores
        if not response.ok:
            raise Exception(f"Error al descargar: {response.status_code}")

        return response.text
