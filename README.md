# Robot Vacuum Cleaners Analysis Project

## Project Overview
This project consists of three main components:
1. Web Crawling: Automated data collection from Swiss e-commerce platforms
2. Data Cleaning: Processing and validating the collected data
3. Analysis & Visualization: Comprehensive market analysis and insights generation

## Web Crawling Process (`product_data.py`)
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
- Identifies and corrects known price errors for specific models
- Validates prices within reasonable range (CHF 50-3000)
- Corrects decimal point errors automatically
- Known corrections include:
  - Samsung Jet Bot Combo AI Steam+
  - Powerology Smart Robotic
  - Neatron Robot hoover
  - Other models with decimal point issues

### Battery Capacity Cleaning
- Corrects major outliers in battery capacity data
- Implements validation range (1,000-10,000 mAh)
- Fixed specific errors for models:
  - Mova P50 Pro Ultra (5,200,000 → 5,200 mAh)
  - Liectroux V3SPro (4,400,000 → 4,400 mAh)
  - Liectroux L200 (2,600,000 → 2,600 mAh)

### General Data Cleaning
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

## Key Findings
- Mid-range segment (CHF 200-500) dominates with 52.8% market share
- Chinese manufacturers hold 29.7% market share
- Average battery life is 169 minutes
- Most models support Amazon Alexa (62.4%) and Google Assistant (53.8%)
- Average customer rating is 4.17/5

## Files in the Repository
- `product_data.py`: Web scraping script for data collection
- `clean_data.py`: Data cleaning and preprocessing script
- `Vacuum_EDA.py`: Exploratory data analysis and visualization script
- `robot_vacuums.csv`: Raw scraped dataset
- `robot_vacuums_cleaned.csv`: Cleaned dataset
- `Vacuum robots info summary.txt`: Detailed analysis report
- `plots/`: Directory containing all visualizations

## Usage
1. Collect data (requires proper setup of web scraping environment):
   ```bash
   python product_data.py
   ```
2. Clean the collected data:
   ```bash
   python clean_data.py
   ```
3. Generate analysis and visualizations:
   ```bash
   python Vacuum_EDA.py
   ```

## Dependencies
- requests
- beautifulsoup4
- pandas
- numpy
- matplotlib
- seaborn

## Future Improvements
- Expand web scraping to additional e-commerce platforms
- Add automated price monitoring over time
- Implement machine learning for price prediction
- Add interactive visualizations
- Expand analysis to include more markets
- Add automated data validation during scraping
- Implement parallel scraping for better performance

## License
This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024 Jiaqi Yu, Lukas Kramer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Contact Information
### Project Maintainers
- **Jiaqi Yu**
  - GitHub: [@Trista1208](https://github.com/Trista1208)
  - Role: Data Analysis & Visualization

- **Lukas Kramer**
  - GitHub: [@LukasDDg](https://github.com/LukasDDg)
  - Role: Web Scraping & Data Collection


For any questions, issues, or collaboration inquiries, please:
1. Open an issue in either repository
2. Contact the maintainers through GitHub
3. Fork the repository and submit pull requests for improvements

We welcome contributions and feedback to improve the project!
