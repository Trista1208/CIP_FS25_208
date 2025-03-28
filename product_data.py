import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# List of URLs to scrape
urls = [
    "https://www.digitec.ch/en/s1/product/xiaomi-x20-max-vacuum-mopping-robot-robot-vacuum-cleaners-49838553",
    "https://www.digitec.ch/en/s1/product/dyson-360-vis-nav-robot-vacuum-robot-vacuum-cleaners-37373337",
    "https://www.digitec.ch/en/s1/product/roborock-s8-maxv-ultra-vacuum-mopping-robot-robot-vacuum-cleaners-43695849",
    "https://www.digitec.ch/en/s1/product/dreame-x50-ultra-complete-vacuum-mopping-robot-robot-vacuum-cleaners-53898302",
    "https://www.digitec.ch/en/s1/product/irobot-roomba-combo-j7-vacuum-mopping-robot-robot-vacuum-cleaners-22503264"
]

def clean_price(price_str):
    # Remove currency symbol and convert to float
    price_str = re.sub(r'[^\d.]', '', price_str)
    try:
        return float(price_str)
    except:
        return None

def extract_features(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract product name
    product_name = soup.find('h1').text.strip()

    # Extract price - updated selector
    price_element = soup.find('div', {'class': 'price'})
    price = None
    if price_element:
        price_text = price_element.text.strip()
        price = clean_price(price_text)

    # Categorize price
    if price is not None:
        if price < 500:
            price_category = 'Budget'
        elif 500 <= price < 1000:
            price_category = 'Mid-Range'
        else:
            price_category = 'High-End'
    else:
        price_category = 'N/A'

    # Extract features from the table
    features = {}
    table = soup.find('table')
    if table:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 2:
                key = cols[0].text.strip()
                value = cols[1].text.strip()
                features[key] = value

    return {
        'Product Name': product_name,
        'Price (CHF)': price,
        'Price Category': price_category,
        **features
    }

# Scrape data from all URLs
data = []
for url in urls:
    try:
        product_data = extract_features(url)
        data.append(product_data)
        print(f"Successfully scraped: {product_data['Product Name']} - Price: {product_data['Price (CHF)']}")
    except Exception as e:
        print(f"Error scraping {url}: {e}")

# Convert data to DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('product_features.csv', index=False)

print("\nData scraping completed and saved to product_features.csv")
print(f"\nTotal products scraped: {len(data)}")


