import os
import csv
from datetime import datetime

# Base directory where the files are downloaded
download_folder = r"C:\Users\birad\OneDrive\Desktop\NSE_BOT\Download"

# Today's date to validate files downloaded for the current day
#today_date = datetime.now().strftime("%d-%b-%Y")

# Path for today's download folder
#download_folder = os.path.join(base_download_folder, today_date)

def validate_file(file_path):
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    # Check file extension
    if not file_path.endswith(".csv"):
        print(f"Invalid file extension for {file_path}. Expected .csv")
        return False

    # Check if the file is empty
    if os.path.getsize(file_path) == 0:
        print(f"File is empty: {file_path}")
        return False

    # Validate CSV headers
    try:
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            headers = next(reader, None)
            if not headers or len(headers) < 2:  # Assuming at least 2 columns are required
                print(f"File {file_path} has invalid headers or is not in the correct format.")
                return False
    except Exception as e:
        print(f"Error reading CSV file {file_path}: {e}")
        return False

    print(f"File {file_path} is valid.")
    return True


def validate_downloaded_files():
    """
    Validates all files in the specified download folder for today's date.

    Checks for:
    - File existence.
    - Correct naming convention (contains today's date).
    - Valid CSV format and headers.

    Prints validation results for each file.
    """
    # Check if the download folder exists
    if not os.path.exists(download_folder):
        print(f"Download folder for today's date does not exist: {download_folder}")
        return

    # List all files in the folder
    files = os.listdir(download_folder)

    if not files:
        print(f"No files found in the download folder: {download_folder}")
        return

    print(f"Validating files in the folder: {download_folder}")

    # Validate each file
    for file_name in files:
        file_path = os.path.join(download_folder, file_name)

        # Check if the file name includes today's date
        if download_folder not in file_name:
            print(f"File name does not include today's date: {file_name}")
            continue

        # Validate the file
        validate_file(file_path)


if __name__ == "__main__":
    # Run the validation process
    validate_downloaded_files()
