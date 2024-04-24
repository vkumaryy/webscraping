# Required module imports
import csv
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# User defined variables for data retrieval
origin = "BOM"  # Origin airport code
destin = "DEL"  # Destination airport code
trDate = sys.argv[1]  # Date as 1st command line argument.

# Base URL for fetching data from MakeMyTrip Website.
baseDataUrl = f"https://www.makemytrip.com/flight/search?itinerary={origin}-{destin}-{trDate}&tripType=0&paxType=A-1_C-0_1-0&intl=false&=&cabinClass=E"

try:
    # Chrome driver is being used.
    driver = webdriver.Chrome()
    print("Requesting URL: " + baseDataUrl)
    driver.get(baseDataUrl)  # URL requested in the browser.
    print("Webpage found ...")

    element_xpath = '//*[@id="left-side--wrapper"]/div[2]'  # First box with relevant flight data.

    # Wait until the first box with relevant flight data appears on Screen
    element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))

    # Scroll the page till bottom to get full data available in the DOM.
    print("Scrolling document upto bottom...")
    for j in range(1, 100):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Find the document body and get its inner HTML for processing in BeautifulSoup parser.
    body = driver.find_element_by_tag_name("body").get_attribute("innerHTML")
    print("Closing Chrome ...")

    # No more usage needed.
    driver.quit()  # Browser Closed.

    print("Getting data from DOM...")
    soupBody = BeautifulSoup(body, 'html.parser')  # Parse the inner HTML using BeautifulSoup

    # Extract the required tags
    spanFlightName = soupBody.findAll("span", {"class": "airways-name"})
    pFlightCode = soupBody.findAll("p", {"class": "fli-code"})
    divDeptTime = soupBody.findAll("div", {"class": "dept-time"})
    pDeptCity = soupBody.findAll("p", {"class": "dept-city"})
    pFlightDuration = soupBody.findAll("p", {"class": "fli-duration"})
    pArrivalTime = soupBody.findAll("p", {"class": "reaching-time append_bottom3"})
    pArrivalCity = soupBody.findAll("p", {"class": "arrival-city"})
    spanFlightCost = soupBody.findAll("span", {"class": "actual-price"})

    # Data Headers
    flightsData = [["flight_name", "flight_code", "departure_time", "departure_city", "flight_duration", "arrival_time", "arrival_city", "flight_cost"]]

    # Extracting data from tags and appending to main database flightsData
    for j in range(0, len(spanFlightName)):
        flightsData.append([
            spanFlightName[j].text,
            pFlightCode[j].text,
            divDeptTime[j].text,
            pDeptCity[j].text,
            pFlightDuration[j].text,
            pArrivalTime[j].text,
            pArrivalCity[j].text,
            spanFlightCost[j].text
        ])

    # Output File for FlightsData.
    outputFile = f"FlightsData_{origin}-{destin}-{trDate.split('/')[0]}-{trDate.split('/')[1]}-{trDate.split('/')[2]}.csv"

    # Publishing Data to File
    print("Writing flight data to file: " + outputFile + "...")
    with open(outputFile, 'w', newline='') as spfile:
        csv_writer = csv.writer(spfile)
        csv_writer.writerows(flightsData)
    print("Data Extracted and Saved to File.")

except Exception as e:
    print("An error occurred:", str(e))
