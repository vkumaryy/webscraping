import requests
import json
import pandas as pd
from bs4 import BeautifulSoup

def scrape_flight_data(origin, destination, travel_date):
    # url = f"https://www.makemytrip.com/flight/search?itinerary={origin}-{destination}-{travel_date}&tripType=0&paxType=A-1_C-0_1-0&intl=false&=&cabinClass=E"

    url = f"https://www.makemytrip.com/flight/search?itinerary={origin}-{destination}-{travel_date}&tripType=O&paxType=A-1_C-0_I-0&intl=false&cabinClass=E&ccde=IN&lang=eng"

    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting flight details
        flights_data = []
        for flight in soup.find_all('div', class_='listingCard'):
            flight_name = flight.find('span', class_='airways-name').text.strip()
            flight_code = flight.find('p', class_='fli-code').text.strip()
            departure_time = flight.find('div', class_='dept-time').text.strip()
            departure_city = flight.find('p', class_='dept-city').text.strip()
            flight_duration = flight.find('p', class_='fli-duration').text.strip()
            arrival_time = flight.find('p', class_='reaching-time').text.strip()
            arrival_city = flight.find('p', class_='arrival-city').text.strip()
            flight_cost = flight.find('span', class_='actual-price').text.strip()

            # Append flight details to the list
            flights_data.append({
                'flight_name': flight_name,
                'flight_code': flight_code,
                'departure_time': departure_time,
                'departure_city': departure_city,
                'flight_duration': flight_duration,
                'arrival_time': arrival_time,
                'arrival_city': arrival_city,
                'flight_cost': flight_cost
            })

        return flights_data

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return None

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Flight data saved to {filename}")

def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Flight data saved to {filename}")

if __name__ == "__main__":
    origin = input("Enter origin airport code: ")
    destination = input("Enter destination airport code: ")
    travel_date = input("Enter travel date (YYYY-MM-DD): ")

    # Scrape flight data
    flights_data = scrape_flight_data(origin, destination, travel_date)

    if flights_data:
        # Save flight data to JSON file
        json_filename = f"FlightsData_{origin}-{destination}-{travel_date}.json"
        save_to_json(flights_data, json_filename)

        # Save flight data to Excel file
        excel_filename = f"FlightsData_{origin}-{destination}-{travel_date}.xlsx"
        save_to_excel(flights_data, excel_filename)
