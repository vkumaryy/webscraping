import requests
from bs4 import BeautifulSoup

# Function to scrape hotel information from TripAdvisor page
def scrape_tripadvisor_hotels(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        hotels = soup.find_all('div', class_='listing_title')  # Hotel names
        reviews = soup.find_all('a', class_='review_count')  # Review counts
        ratings = soup.find_all('span', class_='ui_bubble_rating')  # Ratings

        data = []
        for hotel, review, rating in zip(hotels, reviews, ratings):
            data.append({
                'hotel': hotel.text.strip(),
                'review_count': review.text.strip(),
                'rating': float(rating['alt'].split()[0])  # Extract numerical rating from 'alt' attribute
            })
        return data
    else:
        print("Failed to fetch page:", response.status_code)
        return None

# URL of the TripAdvisor page listing hotels in Lakshadweep
url = "https://www.tripadvisor.in/Hotels-g297640-Lakshadweep-Hotels.html"

# Scrape hotel information
hotel_data = scrape_tripadvisor_hotels(url)

if hotel_data:
    # Display results
    for data in hotel_data:
        print("Hotel:", data['hotel'])
        print("Review Count:", data['review_count'])
        print("Rating:", data['rating'])
        print("\n")
else:
    print("No data scraped.")
