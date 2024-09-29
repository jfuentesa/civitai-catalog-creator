# Civitai Catalog Creator

This project is a PHP application that allows downloading information pages from a list of URLs of CivitAI models.

The application creates HTML files for each type of model, in which it adds all the information about those models and images. Additionally, it allows adding notes to each of the models, starting from personalized HTML files.

## Requirements

- PHP 7.4 or higher
- PHP cURL extension

## Installation

Clone this repository on your local machine or download the project files.
```
git clone https://github.com/jfuentesa/civitai-catalog-creator.git
cd civitai-catalog-creator/
```
## Usage

1. Prepare a text file that contains a list of URLs to process. Each URL should be on a separate line. For example, `urls.txt`:
```
https://...
https:// ...
```

2. Run the program from the command line, providing the file and the destination folder as arguments:
```
php src/civitai-catalog-creator.php urls.txt downloads_folder
```

- **Argument**: The path to the text file containing URLs.
- The program will process each URL, validate whether it has already been downloaded (checking the `processed_ids` file), and if not, download the content and save it.

## `processed_ids` File

The `processed_ids` file contains a list of all IDs that have already been processed. If an ID is already in this file, the program will skip it and not download any data. It analyzes either the URL or the web contents to know if it's necessary to download the data again.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

