# CIP_FS25_208
# Product Data Scraper

This project is a web scraper designed to extract Vacumm robots on the market's information from a list of URLs. It uses Python libraries such as `requests`, `BeautifulSoup`, and `pandas` to fetch, parse, and organize data into a CSV file.

## Features

- Extracts product name, price, and various features from product pages.
- Categorizes products based on price into Budget, Mid-Range, and High-End.
- Saves the extracted data into a CSV file for easy analysis.

## Requirements

- Python 3.12.7
- `requests` library
- `BeautifulSoup` from `bs4` library
- `pandas` library

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/LukasDDg/CIP_FS25_208.git
   cd <repository-directory(may differs)>
   ```

2. Install the required libraries:
   ```bash
   pip install requests beautifulsoup4 pandas
   ```

## Usage

1. Update the `urls` list in `product_data.py` with the product URLs you want to scrape.

2. Run the script:
   ```bash
   python product_data.py
   ```

3. The script will output a `product_features.csv` file containing the scraped data.

## Output

- `product_features.csv`: A CSV file containing the following columns:
  - Product Name
  - Price (CHF)
  - Price Category
  - Various product features extracted from the page

## Notes

- Ensure that the URLs provided are accessible and the page structure matches the expected format for successful scraping.
- The script categorizes prices into three categories: Budget (< 500 CHF), Mid-Range (500-1000 CHF), and High-End (> 1000 CHF).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For any questions or inquiries, please contact us on Github @Trista1208 @LukasDDg.
