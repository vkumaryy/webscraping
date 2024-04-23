import requests
from bs4 import BeautifulSoup

# URL of the website you want to extract data from
url = "https://www.booking.com"

# Send a GET request to the website
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the website
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract data from paragraph and title tags
    paragraphs = soup.find_all("p")
    titles = soup.find_all("title")
    
    # Print the data
    for title in titles:
        print("Title:", title.get_text().strip())
    
    for paragraph in paragraphs:
        print("Paragraph:", paragraph.get_text().strip())
else:
    print("Failed to retrieve data from the website. Status code:", response.status_code)