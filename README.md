# Robot Vacuum Cleaners Analysis Project

## Project Overview
This project consists of four main components:
1. Web Crawling: Automated data collection from Swiss e-commerce platforms
2. Data Cleaning: Processing and validating the collected data
3. Exploratory Data Analysis: Comprehensive market analysis and insights creation
4. Data Analysis: Advanced statistical analysis and feature importance

## Project Files

### Core Files
- `CIP_crawling.py`: Web scraping module for collecting robot vacuum data
- `clean_data.py`: Data cleaning and preprocessing module
- `Vacuum_EDA.py`: Exploratory data analysis and visualization module
- `CIP_analysis.py`: Advanced data analysis module
- `execution.ipynb`: Main notebook that demonstrates the complete workflow

### Data Files
- `robot_vacuums.csv`: Raw scraped dataset
- `robot_vacuums_cleaned.csv`: Cleaned dataset
- `Vacuum robots info summary.txt`: Detailed analysis report
- `Custom_EDA_Report.txt`: Custom EDA report

### Output Directories
- `plots/`: Directory containing all visualizations
- `custom_plots/`: Directory for custom visualizations
- `selective_plots/`: Directory for selective visualizations

## Execution Process
The `execution.ipynb` notebook provides a step-by-step guide through the entire process:

1. **Data Crawling**
   ```python
   from CIP_crawling import crawl_for_links, crawl_for_product_data, data_to_csv
   # Get product URLs from the search results page
   urls = crawl_for_links(url="https://www.galaxus.ch/en/s2/producttype/robot-vacuum-cleaners-174?take=100",
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

   # Scrape all product data and store it in a dictionary
   # [:5] is for testing only. Scraping one product takes approximately 4 seconds, so scraping around 500 products takes about 40 minutes.
   data = crawl_for_product_data(urls[:5],
                                 user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

   # Save the data to a .csv file
   data_to_csv(data, save=False)
   ```

2. **Data Cleaning**
   ```python
   from clean_data import process_data
   
   # Process and clean the robot vacuum data
   df_original, df_cleaned, report = process_data(
       input_file='robot_vacuums.csv',
       output_file='robot_vacuums_cleaned.csv',
       report_file='Vacuum robots info summary.txt'
   )
   ```

3. **Exploratory Data Analysis**
   ```python
   from Vacuum_EDA import eda_default_execution, eda_custom_execution, eda_selective_execution
   
   # These functions allow us to perform different types of evaluations to gain insights from the data.
   # They are optional and not required for the main process.

   # Run the full EDA pipeline with default parameters
   eda_default_execution(input_df='robot_vacuums_cleaned.csv', save_plot=False)

   # Specify custom input and output files, and a directory for plots
   eda_custom_execution(input_df='robot_vacuums_cleaned.csv', save_plot=False)

   # Run only selected analysis functions
   eda_selective_execution(input_file='robot_vacuums_cleaned.csv', save_plot=False)  # Note: this function uses input_file, not input_df
   ```

4. **Data Analysis**
   ```python
   from CIP_analysis import load_new, onehot_encoding, price_efficiency, feature_rating, price_efficiency_features
   
   # Load the cleaned CSV file
   df_cleaned = load_new(new_csv="robot_vacuums_cleaned.csv", print_i=False)

   # Create one-hot encodings from the features
   df_onehot = onehot_encoding(df_cleaned, print_i=False)

   # Calculate the price-efficiency of the products and return the top X products in each category
   price_efficiency(df_onehot, top=5, price_rel=50)

   # Analyze the influence of features on product ratings and display those with the lowest p-values
   feature_rating(df_onehot)

   # Rank features based on price and rating
   price_efficiency_features(df_onehot, print_i=True)
   ```

## Web Crawling Process (`CIP_crawling.py`)
The web scraping component is responsible for collecting robot vacuum data:

### Scraping Features
- Automated data extraction from galaxus.ch
- Collects detailed product specifications including:
  - Product names and models
  - Prices and availability
  - Technical specifications
  - Features and capabilities
  - Customer ratings and reviews
  - Smart home compatibility
  - Surface compatibility information

### Implementation Details
- Uses Selenium with undetected-chromedriver to avoid detection
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

## Data Analysis (`CIP_analysis.py`)
The analysis script performs advanced statistical analysis:

### Feature Engineering
- One-hot encoding of categorical variables
- Feature importance analysis
- Correlation analysis

### Price Efficiency Analysis
- Price-to-feature ratio calculation
- Top products by price efficiency
- Feature-specific price efficiency

### Statistical Analysis
- Regression analysis for feature importance
- Correlation analysis between features and ratings
- Market segmentation analysis

## Requirements

- Python 3.12.7

- for the libraries look at `requirements.txt`


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

1. For the complete workflow, use the Jupyter notebook:
   ```bash
   jupyter notebook execution.ipynb
   ```

2. To run each script separately in order:
   ```bash
   python CIP_crawling.py           # Step 1: Web scraping
   python execute_clean_data.py     # Step 2: Data cleaning
   python Vacuum_EDA.py             # Step 3: Exploratory data analysis
   python CIP_analysis.py           # Step 4: Advanced analysis
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For any questions or inquiries, please contact:
- Jiaqi Yu (Trista1208) - Data Cleaning & Analysis & Visualization
- Lukas Kramer (LukasDDg) - Web Scraping & Data Collection & Analysis
