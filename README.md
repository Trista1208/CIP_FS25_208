# Robot Vacuum Cleaners Analysis Project

## Project Overview
This project consists of three main components:
1. Web Crawling: Automated data collection from Swiss e-commerce platforms
2. Data Cleaning: Processing and validating the collected data
3. Analysis & Visualization: Comprehensive market analysis and insights generation

## Web Crawling Process (`CIP_Crawling.ipynb`)
The web scraping component is responsible for collecting robot vacuum data:

### Scraping Features
- Automated data extraction from digitech.ch
- Collects detailed product specifications including:
  - Product names and models
  - Prices and availability
  - Technical specifications
  - Features and capabilities
  - Customer ratings and reviews
  - Smart home compatibility
  - Surface compatibility information

### Implementation Details
- Uses Python's `requests` and `BeautifulSoup4` libraries
- Implements rate limiting to respect website policies
- Handles different page structures and formats
- Extracts data from dynamic content
- Exports data to structured CSV format

### Error Handling
- Robust error handling for network issues
- Validation of extracted data
- Logging of failed requests
- Retry mechanism for temporary failures

## Data Cleaning Process (`clean_data.py`)
The data cleaning script performs several key operations:

### Price Validation and Correction
- Identifies and corrects price errors
- Validates prices within reasonable range (CHF 50-3000)
- Corrects decimal point errors automatically

### Battery Capacity Cleaning
- Corrects major outliers in battery capacity data
- Implements validation range (1,000-10,000 mAh)
- Fixes decimal point magnitude errors

### General Data Cleaning
- Removes columns with more than 15 empty attributes
- Standardizes column names
- Converts units to numeric values (removing units like 'Pa', 'mAh', etc.)
- Processes list-like columns (features, surfaces, smart home ecosystems)
- Merges color information from multiple columns
- Removes duplicate entries
- Handles missing values

## Exploratory Data Analysis (`Vacuum_EDA.py`)
The EDA script generates various visualizations and analyses:

### Price Analysis
- Distribution of prices across different segments
- Price category breakdown (Budget, Mid-range, Premium, Luxury)
- Price variations by manufacturer and country of origin

### Market Analysis
- Manufacturer market share
- Country of origin distribution
- Brand positioning and pricing strategies

### Technical Analysis
- Battery capacity and life analysis
- Suction power distribution
- Feature availability across price segments

### Created Visualizations
Located in the `plots/` directory:
1. `price_distribution.png`: Overall price distribution
2. `price_category_pie.png`: Market segmentation by price
3. `country_distribution.png`: Market share by country
4. `battery_vs_price.png`: Correlation between battery capacity and price
5. `battery_life_by_price.png`: Battery life across price categories
6. `price_battery_rating.png`: Multi-dimensional analysis
7. `avg_price_by_country.png`: Price variations by country
8. `correlation_matrix.png`: Key metric correlations

## Summary Report
A comprehensive analysis report (`Vacuum robots info summary.txt`) includes:
- Market overview and segmentation
- Manufacturer and country analysis
- Technical specifications summary
- Customer satisfaction metrics
- Key correlations and insights
- Consumer recommendations

## Files in the Repository
- `CIP_Crawling.ipynb`: Web scraping script for data collection
- `clean_data.py`: Data cleaning and preprocessing script
- `Vacuum_EDA.py`: Exploratory data analysis and visualization script
- `robot_vacuums.csv`: Raw scraped dataset
- `robot_vacuums_cleaned.csv`: Cleaned dataset
- `Vacuum robots info summary.txt`: Detailed analysis report
- `plots/`: Directory containing all visualizations

## Requirements

- Python 3.12.7
- `requests` library
- `BeautifulSoup` from `bs4` library
- `pandas` library
- `numpy` library
- `matplotlib` library
- `seaborn` library

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/LukasDDg/CIP_FS25_208.git
   cd CIP_FS25_208
   ```

2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the data cleaning script:
   ```bash
   python clean_data.py
   ```

2. Generate analysis and visualizations:
   ```bash
   python Vacuum_EDA.py
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For any questions or inquiries, please contact:
- Jiaqi Yu (Trista1208) - Data Analysis & Visualization
- Lukas Kramer (LukasDDg) - Web Scraping & Data Collection
