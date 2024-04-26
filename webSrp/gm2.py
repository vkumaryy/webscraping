import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_website(url, save_excel=True):
    """Scrapes data from a website URL and returns it as JSON or text, optionally saving to an Excel sheet.

    Args:
        url (str): The URL of the website to scrape.
        save_excel (bool, optional): Whether to save the extracted data to an Excel sheet. Defaults to True.

    Returns:
        dict or str: The extracted data in JSON format if successfully parsed, otherwise in plain text.
    """

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text from desired tags (adjust as needed)
        extracted_data = []
        for tag in ['p', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'span', 'div']:
            elements = soup.find_all(tag)
            for element in elements:
                text = element.get_text(strip=True)  # Remove leading/trailing whitespace
                if text:
                    extracted_data.append(text)

        # Handle JSON parsing or return raw text
        try:
            json_data = json.loads(''.join(extracted_data))  # Attempt JSON parsing
            return json_data
        except json.JSONDecodeError:
            return '\n'.join(extracted_data)  # Return raw text if JSON parsing fails

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return "Error fetching URL"

    except Exception as e:
        print(f"An error occurred: {e}")
        return f"Error: {e}"

    if save_excel:
        try:
            df = pd.DataFrame(extracted_data, columns=['Extracted Text'])
            df.to_excel('scraped_data.xlsx', index=False)
            print("Data saved to scraped_data.xlsx")
        except pd.errors.ExcelFileError as e:
            print(f"Error saving to Excel: {e}")

if __name__ == '__main__':
    url = input("Enter the URL to scrape: ")
    extracted_data = scrape_website(url)
    print("Extracted data:")
    print(extracted_data)
