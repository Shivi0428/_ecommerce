import requests
from bs4 import BeautifulSoup

# URL of the page to be scraped
url = "https://aws.amazon.com/ec2/instance-types/"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, "html.parser")

# Find the sections containing instance types
instance_sections = soup.find_all('div', class_='lb-content-item')

# List to store VM configurations
vm_configurations = []

# Loop through each section and extract information
for section in instance_sections:
    title = section.find('h2').get_text(strip=True)
    details = section.find_all('p')
    detail_text = [detail.get_text(strip=True) for detail in details]

    vm_configurations.append({
        'title': title,
        'details': detail_text
    })

# Save the scraped data to a file
import json

with open('mt_vm_configurations.json', 'w') as file:
    json.dump(vm_configurations, file)
