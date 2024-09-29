# Civitai Catalog Creator

This project is a Python application that allows downloading information pages from a list of URLs of CivitAI models.

The application creates HTML files for each type of model, in which it adds all the information about those models and images. Additionally, it allows adding notes to each of the models, starting from personalized HTML files.

## Requirements

- Python 3.11 or higher

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
python src/civitai-catalog-creator.py urls.txt downloads_folder
```

The program will process each URL, validate whether it has already been downloaded (checking the `processed_ids` file), and if not, download the content and save it in the specified folder.

## The `processed_ids` file

The `processed_ids` file contains a list of all IDs that have already been processed. If an ID is already in this file, the program will skip it and not download any data. It analyzes either the URL or the web contents to know if it's necessary to download the data again.

## Custom contents

To add custom content, you can create a folder called `custom` within the root directory of the execution. Inside this folder, create HTML files with names that match the ID of the model whose content you want to include.

For example, if you want to include the content of a model with ID `123`, create an HTML file named `custom/123.html`. The content of this file will be automatically included in the generated HTML for the corresponding model.

## Demo

In the `demo` folder, you'll find all the content produced by running the script with the `urls` file that includes the URLs.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

