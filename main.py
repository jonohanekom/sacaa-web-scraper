import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

# URL of the page to scrape
url = "https://www.caa.co.za/industry-information/aeronautical-information-aeronautical-charts/"

# Directory where the PDFs will be saved
save_dir = "pdfs"

# Create directory if it doesn't exist
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Function to download a PDF
def download_pdf(pdf_url, save_path):
    response = requests.get(pdf_url)
    with open(save_path, 'wb') as file:
        file.write(response.content)
    print(f"Downloaded: {save_path}")

# Send a GET request to the page
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

            # Download the PDF
            download_pdf(pdf_url, save_path)
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
