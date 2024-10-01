import os
import re
import shutil


def restructure_files_by_icao(directory):
    """
    This function moves PDF files in a given directory into subfolders based on ICAO codes
    found in the filenames, ignoring any characters after the ICAO code.

    :param directory: Path to the directory containing the files to be restructured
    """
    
    def extract_icao_code(filename):
        """
        Extracts the first 4-letter ICAO code from a filename using a regular expression.
        Ignores any characters that come after the ICAO code.

        :param filename: Name of the file
        :return: The ICAO code if found, otherwise None
        """
        match = re.search(r'\b[A-Z]{4}', filename)
        if match:
            return match.group(0)  # Return the first 4 characters as the ICAO code
        return None

    # Get a list of PDF files in the specified directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.lower().endswith('.pdf')]
    
    # Process each file
    for file in files:
        icao_code = extract_icao_code(file)
        
        if icao_code:
            # Create a folder for the ICAO code if it doesn't exist
            icao_folder = os.path.join(directory, icao_code)
            if not os.path.exists(icao_folder):
                os.makedirs(icao_folder)
            
            # Move the file into the corresponding ICAO code folder
            original_file_path = os.path.join(directory, file)
            new_file_path = os.path.join(icao_folder, file)
            shutil.move(original_file_path, new_file_path)
            print(f"Moved: {file} to {icao_folder}")

# Example usage:
directory_path = '/Users/jonathanhanekom/Desktop/projects/sacaa-web-scraper/sacaa-web-scraper/pdfs'
restructure_files_by_icao(directory_path)
