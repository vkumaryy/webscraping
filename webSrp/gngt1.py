import requests
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download the VADER lexicon if not already downloaded
nltk.download('vader_lexicon')

# Initialize the sentiment analyzer
sid = SentimentIntensityAnalyzer()

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
    titles = soup.find_all("h3", class_="bui-f-font-display_two")
    
    # Combine all text data into a single string
    all_text = ""
    for title in titles:
        all_text += title.get_text() + " "
    
    for paragraph in paragraphs:
        all_text += paragraph.get_text() + " "
    
    # Perform sentiment analysis on the combined text
    sentiment = sid.polarity_scores(all_text)
    
    # Print the sentiment analysis result
    print("Sentiment analysis result for the whole data:")
    print(sentiment)
else:
    print("Failed to retrieve data from the website. Status code:", response.status_code)