# Tool for Scanning Browser Extensions

This CLI tool is designed to process Excel files, focusing on Google Chrome and Mozilla Firefox Extension IDs. It fetches permissions and other details from the Crxcavator API and writes the processed data to Excel files.

## Credits

Credit for the API and platform belongs to CRXcavator by DUO Security (https://crxcavator.io/). This script automates interactions with their API.

## Installation

~~~
git clone https://github.com/Ephemaral/extension_scanner.git

cd extension_scanner

pip install -r requirements.txt
~~~

## Usage

1. **Prepare Your Excel File**:
   - Your Excel file should contain Extension IDs in a single cell separated by commas or in multiple cells. Ensure there is no other data in the sheet.

2. **Run the Scanner**:
   - To scan a file, use the following command, replacing `<file_name.xlsx>` with the path to your Excel file:
python3 scanner.py <file_name.xlsx>

- For testing purposes, you can use the provided test file:

~~~
python3 scanner.py test.xlsx
~~~


## Prerequisites

- **Python 3**: Ensure you have Python 3 installed on your system.
- **Excel File**: Prepare an Excel file with Extension IDs. The file can contain IDs in a single cell separated by commas or in multiple cells.

## Additional Tips

- **Single Extension ID**: If you only want to scan a single Extension ID, you can directly use the CRXcavator website (https://crxcavator.io/), which supports Google Chrome, Firefox, and Opera.
- **Contributions**: Feel free to contribute to this project by submitting pull requests or reporting issues.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
