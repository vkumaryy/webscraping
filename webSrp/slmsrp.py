from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode, i.e., without opening a browser window

# Set up Chrome WebDriver
s = Service("/usr/bin/chromedriver")  # Path to your chromedriver executable
driver = webdriver.Chrome(service=s, options=chrome_options)

# URL of the website you want to extract data from
url = "https://www.booking.com"

# Load the webpage
driver.get(url)

# Wait for dynamic content to load (adjust sleep time as needed)
time.sleep(5)  # Wait for 5 seconds

# Extract data using Selenium
titles = driver.find_elements(By.CLASS_NAME, "bui-f-font-display_two")  # Titles
paragraphs = driver.find_elements(By.TAG_NAME, "p")  # Paragraphs

# Print the extracted data
print("Titles:")
for title in titles:
    print(title.text)

print("\nParagraphs:")
for paragraph in paragraphs:
    print(paragraph.text)

# Quit the WebDriver
driver.quit()