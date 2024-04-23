import requests
from bs4 import BeautifulSoup

# Make a request to the webpage
url = "https://holidayz.makemytrip.com/holidays/india/package?id=37167&listingClassId=2519&pkgType=FIT&fromCity=Kolkata&defaultPageForOnlineBookableFIT=true&intid=Seo_DOM_Holiday_pkg_name_click&affiliate=MMT&mcat=Romantic,Family&depDate=2024-06-23&room=2,0,0,0,,,"  # Replace with the actual URL of the travel booking page
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Extract the required information from the webpage
# Use BeautifulSoup methods and navigate through the HTML structure to find specific elements and their content

# Example: Extract all hotel names
hotel_names = soup.find_all("h3", class_="hotel-name")
for name in hotel_names:
    print(name.text)

# Example: Extract all prices
prices = soup.find_all("span", class_="price")
for price in prices:
    print(price.text)

# Continue extracting other relevant data as per your requirements