import csv
import sys
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_flight_data(origin, destination, travel_date):
    # Base URL for fetching data from MakeMyTrip Website.
    base_url = f"https://www.makemytrip.com/flight/search?itinerary={origin}-{destination}-{travel_date}&tripType=0&paxType=A-1_C-0_1-0&intl=false&=&cabinClass=E"

    try:
        # Chrome driver setup
        driver = webdriver.Chrome()
        print("Requesting URL: " + base_url)
        driver.get(base_url)  # URL requested in the browser.
        print("Webpage found ...")

        element_xpath = '//*[@id="left-side--wrapper"]/div[2]'  # First box with relevant flight data.

        # Wait until the first box with relevant flight data appears on Screen
        element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))

        # Scroll the page till bottom to get full data available in the DOM.
        print("Scrolling document up to bottom...")
        for j in range(1, 100):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Find the document body and get its inner HTML for processing in BeautifulSoup parser.
        body = driver.find_element_by_tag_name("body").get_attribute("innerHTML")
        print("Closing Chrome ...")

        # No more usage needed.
        driver.quit()  # Browser Closed.

        print("Getting data from DOM...")
        # Parse the inner HTML using BeautifulSoup
        soup = BeautifulSoup(body, 'html.parser')

        # Extract the required tags
        span_flight_name = soup.findAll("span", {"class": "airways-name"})
        p_flight_code = soup.findAll("p", {"class": "fli-code"})
        div_dept_time = soup.findAll("div", {"class": "dept-time"})
        p_dept_city = soup.findAll("p", {"class": "dept-city"})
        p_flight_duration = soup.findAll("p", {"class": "fli-duration"})
        p_arrival_time = soup.findAll("p", {"class": "reaching-time append_bottom3"})
        p_arrival_city = soup.findAll("p", {"class": "arrival-city"})
        span_flight_cost = soup.findAll("span", {"class": "actual-price"})

        # Data Headers
        flights_data = [["flight_name", "flight_code", "departure_time", "departure_city",
                         "flight_duration", "arrival_time", "arrival_city", "flight_cost"]]

        # Extracting data from tags and appending to main database flights_data
        for j in range(0, len(span_flight_name)):
            flights_data.append([
                span_flight_name[j].text,
                p_flight_code[j].text,
                div_dept_time[j].text,
                p_dept_city[j].text,
                p_flight_duration[j].text,
                p_arrival_time[j].text,
                p_arrival_city[j].text,
                span_flight_cost[j].text
            ])

        # Output File for FlightsData.
        output_file = f"FlightsData_{origin}-{destination}-{travel_date}.csv"

        # Publishing Data to File
        print("Writing flight data to file: " + output_file + "...")
        with open(output_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(flights_data)
        print("Data Extracted and Saved to File.")

    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py <origin> <destination> <travel_date>")
        print("Example: python script.py BOM DEL 2024-07-24")
        sys.exit(1)
    origin = sys.argv[1]
    destination = sys.argv[2]
    travel_date = sys.argv[3]
    scrape_flight_data(origin, destination, travel_date)
