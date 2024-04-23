import requests
from bs4 import BeautifulSoup

def scrape_travel_data(url, target_elements):
    """
    Extracts specific data from a travel booking page using Beautiful Soup.

    Args:
        url (str): The URL of the travel booking page.
        target_elements (dict): A dictionary mapping HTML element tags to
                                 desired attributes for data extraction.

    Returns:
        list: A list of dictionaries, where each dictionary represents
              extracted data for a travel listing.
    """

    try:
        response = requests.get(url, headers={'User-Agent': 'My Travel Scraper'})
        response.raise_for_status()  # Raise exception for non-200 status codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    extracted_data = []
    for element_tag, attributes in target_elements.items():
        listings = soup.find_all(element_tag, attrs=attributes)
        for listing in listings:
            data = {}
            for attr_name, attr_value in attributes.items():
                value = listing.get(attr_name)
                if value:
                    data[attr_name] = value.strip()
            extracted_data.append(data)

    return extracted_data

if __name__ == '__main__':
    # Replace with the actual travel booking page URL
    url = "https://holidayz.makemytrip.com/holidays/india/package?id=37167&listingClassId=2519&pkgType=FIT&fromCity=Kolkata&defaultPageForOnlineBookableFIT=true&intid=Seo_DOM_Holiday_pkg_name_click&affiliate=MMT&mcat=Romantic,Family&depDate=2024-06-23&room=2,0,0,0,,,"

    # Example target elements (adjust based on website structure)
    target_elements = {
        "div": {"class": "listing-item"},  # Modify class name if needed
        "h3": {"class": "listing-title"},  # Modify class name if needed
        "span": {"class": "price"},       # Modify class name if needed
        "p": {"class": "review-snippet"}  # Modify class name if needed (optional)
    }

    scraped_data = scrape_travel_data(url, target_elements)

    if scraped_data:
        print("Extracted data:")
        for item in scraped_data:
            print(item)
    else:
        print("No data found or error occurred.")
