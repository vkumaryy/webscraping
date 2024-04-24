# Required module imports

3 import csv

4 import selenium.webdriver

5 from bs4 import BeautifulSoup

6 from selenium.webdriver.support.ui import WebDriverWait

7 from selenium.webdriver.common.by import By

8 from selenium.webdriver.support import expected_conditions as EC

9

10

11 User defined variables for data retreival

12 origin = "BOM"

# Origin airport code

13 destin = "DEL"

# Destination airport code

# Date as 1st command line argument.

14 trDate = sys.argv[1]

15

16

***The following is the Base Url for fetching data from MakeMyTrip Website.

17

This URL appears in the search bar after origin, destination and date inputs on the

landing page. Thus, this URL can be changed based on User Inputs and required data can be fetched.

18

19

baseDataUrl = "https://www.makemytrip.com/flight/search?itinerary="+ origin +"-"+ destin +"-"+ trDate +"&tripType=0&paxType=A-1_C-0_1-0&intl=false&=&cabinClass=E"

20

21


try:

driver selenium.webdriver.Chrome() = Chrome driver is being used.

print ("Requesting URL: " + baseDataUrl)

driver.get(baseDataUrl)

#URL requested in browser.

print ("Webpage found ...")

element_xpath = '//*[@id="left-side--wrapper"]/div[2]' # First box th relevant flight data.

# Wait until the first box with relevant flight data appears on Screen element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, element_xpath))

#Scroll the page till bottom to get full data available in the DOM.

print ("Scrolling document upto bottom...")

for j in range(1, 100):

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Find the document body and get its inner HTML for processing in BeautifulSoup parser.

body = driver.find_element_by_tag_name("body").get_attribute("innerHTML")

print("Closing Chrome ...")

# No more usage needed.

driver.quit()

#Browser Closed.

ons


43

44

45

46

47

48

49

print("Getting data from DOM...")

soupBody = BeautifulSoup (body) # Parse the inner HTML using BeautifulSoup

#Extract the required tags

spanFlightName = soupBody.findAll("span", {"class": "airways-name "})

#Tags with Flight Name

pFlightCode = soupBody.findAll("p", {"class": "fli-code"})

#Tags with Flight Code

50

51

divDeptTime = soupBody.findAll("div", {"class": "dept-time"}) pDeptCity = soupBody.findAll("p", {"class": "dept-city"})

#Tags with Departure Time

52

53

54

pFlightDuration = soupBody.findAll("p", {"class": "fli-duration"})

#Tags with Departure City

#Tags with Flight Duration

pArrivalTime = soupBody.findAll("p", {"class": "reaching-time append_bottom3"}

pArrivalCity = soupBody.findAll("p", {"class": "arrival-city"})

) # Tags with Arrival Time

55

56

spanFlightCost = soupBody.findAll("span", {"class": "actual-price"})

#Tags with Arrival City

#Tags with Flight Cost


#Data Headers

flightsData = [["flight_name", "flight_code", "departure_time", "departure_city", "flight_duration", arrival_time", "arrival_city", "flight_cost"]]

# Extracting data from tags and appending to main database flightsData

for j in range(0, len(spanFlightName)):

flightsData.append([spanFlightName[j].text, pFlightCode[j].text, divDeptTime[j].text, pDeptCity[j]. text, pFlightDuration[j].text, pArrivalTime[j].text, pArrivalCity[j].text, spanFlight Cost[j]. text])

64


4

5

6 7 8 59 70 71 72 73 74

#Output File for FlightsData. This file will have the data in comma separated form.

outputFile = "FlightsData_" + origin +"-"+ destin +"-"+ trDate.split("/")[0] + "-" + trDate.split("/")[1

]+"-" + trDate.split("/") [2] + ".csv"

#Publishing Data to File

print("Writing flight data to file: "+ outputFile + "...")

with open(outputFile, 'w', newline='") as spfile:

csv_writer = csv.writer(spfile) csv_writer.writerows (flightsData)

print ("Data Extracted and Saved to File. ")