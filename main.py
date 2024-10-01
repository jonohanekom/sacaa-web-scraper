import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import shutil
import time

def pdf_downloader():
    # URL to scrape
    url = "https://www.caa.co.za/industry-information/aeronautical-information-aeronautical-charts/"

    # Directory to save PDFs
    save_dir = "pdfs"

    # Create directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Function to download the PDF with retry logic
    def download_pdf(pdf_url, save_path, max_retries=3, retry_delay=5):
        retries = 0
        while retries < max_retries:
            try:
                response = requests.get(pdf_url, timeout=10)  # Adding timeout to prevent hanging
                response.raise_for_status()  # Raise an exception for HTTP errors
                with open(save_path, 'wb') as file:
                    file.write(response.content)
                print(f"Downloaded: {save_path}")
                return True  # Success, exit the loop
            except requests.exceptions.RequestException as e:
                retries += 1
                print(f"Failed to download {pdf_url}. Attempt {retries} of {max_retries}. Error: {e}")
                if retries < max_retries:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"Max retries reached. Skipping: {pdf_url}")
                    return False  # Failure after max retries

    # Send a GET request to the URL
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all links on the page
        for link in soup.find_all('a', href=True):
            href = link['href']

            # Check if the link is a PDF file
            if href.endswith(".pdf"):
                pdf_url = urllib.parse.urljoin(url, href)  # Resolve relative URLs
                pdf_name = os.path.basename(href)
                save_path = os.path.join(save_dir, pdf_name)

                # Check if the file already exists
                if os.path.exists(save_path):
                    print(f"File already exists: {save_path}. Skipping download.")
                else:
                    # Download the PDF with retry logic
                    download_pdf(pdf_url, save_path)
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

pdf_downloader()
