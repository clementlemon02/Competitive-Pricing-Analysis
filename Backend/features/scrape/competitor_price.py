import requests
from bs4 import BeautifulSoup

# URL of the webpage
url = 'https://www.singapore-tickets.com/'

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find the <ul> tag with the specified class
ul_tag = soup.find('ul', class_='styles__StyledNestedMenuContainer-sc-1baztf1-0 kteUaW')

# Initialize an empty list to store label-url pairs
label_url_pairs = []

# If the <ul> tag is found
if ul_tag:
    # Find all <a> tags within the <ul> tag
    links = ul_tag.find_all('a')
    
    # Extract the text and href attributes from each <a> tag
    for link in links:
        label = link.text.strip() 
        url = link['href']          
        label_url_pairs.append((label, url))  


label_datatgid_dict = {}

for label, url in label_url_pairs:

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all elements with the attribute 'data-tgid'
    data_tgid_values = [element['data-tgid'] for element in soup.find_all(attrs={"data-tgid": True})]
    if data_tgid_values:
        label_datatgid_dict[label] = data_tgid_values

# Initialize an empty dictionary to store ticket information
ticket_info = {}

# Iterate over each label and its corresponding data-tgid values
for label, data_tgid_values in label_datatgid_dict.items():
    for data_tgid in data_tgid_values:
        # Construct the URL using the data-tgid value
        url = f"https://book.singapore-tickets.com/book/{data_tgid}/"
        # Send a GET request to the URL
        response = requests.get(url)
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the price element
        price_element = soup.find("span", class_="tour-price")
        # Find the name element
        name_element = soup.find("h3", class_="TextBlock__Text-sc-hd2jvz-0 eUdoQg block")
        if price_element and name_element:
            # Extract ticket price and name
            ticket_price = price_element.text.strip()
            ticket_name = name_element.text.strip()
            ticket_key = f"{label} - {ticket_name}"

            ticket_info[ticket_key] = ticket_price

# Print the dictionary
# print(ticket_info)


# To export the info into csv file
import csv

# Your dictionary containing the data
data = ticket_info

# Specify the file path for the CSV file
csv_file_path = 'output.csv'

# Open the CSV file in write mode
with open(csv_file_path, 'w', newline='') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)
    
    # Write the header row (optional)
    csv_writer.writerow(['Ticket', 'Price'])  # Modify this line based on your data structure
    
    # Write each key-value pair from the dictionary as a row in the CSV file
    for key, value in data.items():
        csv_writer.writerow([key, value])

print(f"CSV file '{csv_file_path}' has been created successfully.")


