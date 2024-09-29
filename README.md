# Civitai Catalog Creator

Este proyecto es una aplicación PHP que permite descargar las páginas de información a partir de una lista de URLs de modelos de CivitAI.

La aplicación crea archivos HTML para cada tipo de modelo, en la que agregará toda la información de esos modelos, y las imágenes.

Además, permite agregar notas a cada uno de los modelos, partiendo de archivos HTML personalizados.

## Requisitos

- PHP 7.4 o superior
- Extensión `cURL` de PHP

## Instalación

Clona este repositorio en tu máquina local o descarga los archivos del proyecto.

```bash
git clone https://github.com/jfuentesa/civitai-catalog-creator.git
cd civitai-catalog-creator
```

## Uso

1. Prepara un archivo de texto que contenga una lista de URLs a procesar. Cada URL debe estar en una línea separada. Por ejemplo, `urls.txt`:

```
https://...
https://...
```

2. Ejecuta el programa desde la línea de comandos, proporcionando la ruta del archivo de URLs como argumento:

```bash
php src/civitai-catalog-creator.php urls.txt
```

- **Argumento**: La ruta al archivo de texto con las URLs.
- El programa procesará cada URL, validará si ya ha sido descargada (consultando el archivo `processed`), y si no lo ha sido, descargará el contenido y lo guardará.

## Archivo `processed_ids`

El archivo `processed_ids` contiene una lista de todas las ids que ya han sido procesadas. Si una id ya está en este archivo, el programa la omitirá y no realizará la descarga de datos, pero sí reescribirá los datos desde la caché HTML.

## Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.
