import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import os

"""
Robot Vacuum Exploratory Data Analysis (EDA) Utility

This module provides functions to analyze robot vacuum data and generate 
visualizations and reports. It can be used as a standalone script or 
imported into other files to use its functions.
"""

def setup_visualization_style():
    """
    Set up the visualization style for consistent and appealing plots.
    """
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")

def ensure_plots_directory(plots_dir='plots'):
    """
    Create a directory for saving plots if it doesn't exist.
    
    The directory specified by plots_dir will be created if it doesn't
    already exist in the file system.
    
    This function takes a plots_dir parameter which defaults to 'plots'
    if not specified.
    """
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)

def get_country(manufacturer):
    """
    Extract country information from manufacturer names and known brands.
    
    This function analyzes the manufacturer name and tries to determine
    the country of origin based on known brand associations.
    
    It takes a manufacturer name as input and returns the identified
    country as a string. If the country can't be determined, it returns 'Other'.
    """
    manufacturer = str(manufacturer).lower()
    if any(brand in manufacturer for brand in ['xiaomi', 'roborock', 'ecovacs', 'dreame']):
        return 'China'
    elif any(brand in manufacturer for brand in ['irobot', 'neato']):
        return 'USA'
    elif any(brand in manufacturer for brand in ['samsung', 'lg']):
        return 'South Korea'
    elif any(brand in manufacturer for brand in ['vorwerk', 'miele', 'bosch', 'karcher']):
        return 'Germany'
    elif any(brand in manufacturer for brand in ['philips']):
        return 'Netherlands'
    else:
        return 'Other'

def add_derived_columns(df):
    """
    Add derived columns to the dataframe for enhanced analysis.
    
    This function enriches the dataframe with additional columns like:
    - price_category: categorizes products by price range
    - country: determines country of origin based on manufacturer
    - rating_category: groups products by rating range
    
    It works with a dataframe of robot vacuum data and returns a new
    dataframe with all the additional columns, leaving the original unchanged.
    """
    # Create a copy to avoid modifying the original
    df = df.copy()
    
    # Create price categories
    price_bins = [0, 200, 500, 1000, float('inf')]
    price_labels = ['Budget (< CHF 200)', 'Mid-range (CHF 200-500)', 'Premium (CHF 500-1000)', 'Luxury (> CHF 1000)']
    df['price_category'] = pd.cut(df['price'], bins=price_bins, labels=price_labels)
    
    # Add country information
    df['country'] = df['manufacturer'].apply(get_country)
    
    # Add rating categories
    rating_bins = [0, 3, 4, 4.5, 5]
    rating_labels = ['Below Average (< 3)', 'Good (3-4)', 'Very Good (4-4.5)', 'Excellent (4.5-5)']
    df['rating_category'] = pd.cut(df['rating'], bins=rating_bins, labels=rating_labels)
    
    return df

def plot_price_distribution(df, save_dir='plots'):
    """
    Create and save a histogram showing the distribution of vacuum prices.
    
    This function visualizes how prices are distributed across the dataset,
    adding helpful reference lines for the mean and median prices.
    
    You need to provide a dataframe with robot vacuum data. The save_dir 
    parameter lets you specify where to save the generated plot.
    """
    plt.figure(figsize=(12, 6))
    sns.histplot(data=df, x='price', bins=30, kde=True)
    plt.title('Distribution of Robot Vacuum Prices')
    plt.xlabel('Price (CHF)')
    plt.ylabel('Count')
    # Add mean and median lines
    plt.axvline(df['price'].mean(), color='red', linestyle='--', label=f'Mean: CHF {df["price"].mean():.2f}')
    plt.axvline(df['price'].median(), color='green', linestyle='--', label=f'Median: CHF {df["price"].median():.2f}')
    plt.legend()
    plt.savefig(f'{save_dir}/price_distribution.png')
    plt.close()

def plot_price_category_pie(df, save_dir='plots'):
    """
    Create and save a pie chart showing the distribution of price categories.
    
    This visualization helps understand how products are distributed across
    different price segments in the market.
    
    You'll need to provide a dataframe with robot vacuum data that includes
    a price_category column. The function returns the price distribution data
    which you can use for further analysis.
    """
    plt.figure(figsize=(10, 6))
    price_dist = df['price_category'].value_counts()
    plt.pie(price_dist, labels=price_dist.index, autopct='%1.1f%%', startangle=90)
    plt.title('Distribution of Robot Vacuums by Price Category')
    plt.axis('equal')
    plt.savefig(f'{save_dir}/price_category_pie.png')
    plt.close()
    
    return price_dist

def plot_country_distribution(df, save_dir='plots'):
    """
    Create and save a pie chart visualizing the country of origin distribution.
    
    This chart shows how robot vacuums in the dataset are distributed
    across different countries of manufacture, with percentages clearly labeled.
    
    The function works with a dataframe containing robot vacuum data and
    returns the country distribution data for potential further analysis.
    You can specify where to save the plot using the save_dir parameter.
    """
    plt.figure(figsize=(12, 8))
    country_dist = df['country'].value_counts()
    # Calculate percentages
    sizes = country_dist.values
    percentages = [f'{(x/sum(sizes)*100):.1f}%' for x in sizes]
    # Create custom labels with both country and percentage
    labels = [f'{country}\n({pct})' for country, pct in zip(country_dist.index, percentages)]

    # Create pie chart with improved styling
    plt.pie(sizes, labels=labels, 
            autopct='',  # Remove internal percentage as we have it in labels
            startangle=90,
            colors=sns.color_palette("husl", n_colors=len(country_dist)),
            wedgeprops={'edgecolor': 'white', 'linewidth': 2})

    plt.title('Distribution of Robot Vacuums by Country of Origin', pad=20, size=14)
    plt.axis('equal')

    # Add a legend
    plt.legend(labels, title="Countries", 
              loc="center left", 
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.savefig(f'{save_dir}/country_distribution.png', bbox_inches='tight', dpi=300)
    plt.close()
    
    return country_dist

def plot_battery_vs_price(df, save_dir='plots'):
    """
    Create and save a scatter plot examining battery capacity vs price.
    
    This visualization helps identify the relationship between a vacuum's
    battery capacity and its price, including a trend line to highlight
    the overall correlation.
    
    The function takes a dataframe with robot vacuum data and saves the plot
    to the specified directory.
    """
    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=df, x='battery_capacity', y='price', alpha=0.6)
    plt.title('Battery Capacity vs Price')
    plt.xlabel('Battery Capacity (mAh)')
    plt.ylabel('Price (CHF)')
    # Add trend line
    df_clean = df.dropna(subset=['battery_capacity', 'price'])
    z = np.polyfit(df_clean['battery_capacity'], df_clean['price'], 1)
    p = np.poly1d(z)
    plt.plot(df_clean['battery_capacity'], p(df_clean['battery_capacity']), "r--", alpha=0.8, label='Trend Line')
    plt.legend()
    plt.savefig(f'{save_dir}/battery_vs_price.png')
    plt.close()

def plot_battery_life_by_price(df, save_dir='plots'):
    """
    Create and save a box plot showing battery life distribution by price category.
    
    This visualization reveals how battery life varies across different price
    segments, helping identify if higher-priced models consistently offer
    longer battery life.
    
    You'll need to provide a dataframe with robot vacuum data. The plot is
    saved to the directory specified by save_dir.
    """
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df[df['battery_life'] <= 500], x='price_category', y='battery_life')
    plt.title('Battery Life Distribution by Price Category\n(Showing robots with battery life ≤ 500 minutes)', pad=20)
    plt.xlabel('Price Category', labelpad=10)
    plt.ylabel('Battery Life (minutes)', labelpad=10)
    plt.ylim(0, 500)  # Set y-axis limits
    plt.grid(True, alpha=0.3)  # Add light grid
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{save_dir}/battery_life_by_price.png', bbox_inches='tight', dpi=300)
    plt.close()

def plot_price_battery_rating(df, save_dir='plots'):
    """
    Create a scatter plot of price vs battery capacity colored by rating.
    
    This multi-dimensional visualization shows how price relates to battery
    capacity while also indicating each product's rating through color coding.
    It helps identify potential sweet spots of value in the market.
    
    The function works with a dataframe of robot vacuum data and saves
    the plot to your specified directory.
    """
    fig = plt.figure(figsize=(12, 8))
    scatter = plt.scatter(df['battery_capacity'], df['price'], 
                         c=df['rating'], cmap='viridis', 
                         alpha=0.6, s=100)
    plt.colorbar(scatter, label='Rating')
    plt.title('Price vs Battery Capacity (colored by Rating)')
    plt.xlabel('Battery Capacity (mAh)')
    plt.ylabel('Price (CHF)')
    plt.tight_layout()
    plt.savefig(f'{save_dir}/price_battery_rating.png')
    plt.close()

def plot_avg_price_by_country(df, save_dir='plots'):
    """
    Create a bar plot showing the average price of vacuums by country of origin.
    
    This visualization helps identify which countries produce higher-end or
    budget-friendly robot vacuums on average.
    
    The function needs a dataframe with robot vacuum data, saves the plot to
    the specified directory, and returns the average price by country data
    which you can use for further analysis.
    """
    plt.figure(figsize=(10, 6))
    avg_price_by_country = df.groupby('country')['price'].mean().sort_values(ascending=False)
    avg_price_by_country.plot(kind='bar')
    plt.title('Average Price by Country of Origin')
    plt.xlabel('Country')
    plt.ylabel('Average Price (CHF)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{save_dir}/avg_price_by_country.png')
    plt.close()
    
    return avg_price_by_country

def plot_correlation_matrix(df, save_dir='plots'):
    """
    Create a heatmap showing correlations between key vacuum metrics.
    
    This visualization helps identify how different features (price, battery
    capacity, battery life, and rating) relate to each other. Strong
    correlations might indicate important relationships in the data.
    
    The function takes a dataframe with robot vacuum data, saves the
    correlation matrix plot to the specified directory, and returns the
    correlation matrix itself for further analysis.
    """
    correlation_matrix = df[['price', 'battery_capacity', 'battery_life', 'rating']].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Matrix')
    plt.tight_layout()
    plt.savefig(f'{save_dir}/correlation_matrix.png')
    plt.close()
    
    return correlation_matrix

def print_summary_statistics(df, price_dist, country_dist, avg_price_by_country):
    """
    Print key summary statistics about the robot vacuum dataset.
    
    This function outputs important statistical information including:
    - Distribution of products across price categories
    - Distribution by country of origin
    - Average prices by country
    - Battery statistics
    
    You'll need to provide the dataframe and the distribution data from
    previous analysis functions.
    """
    print("\nSummary Statistics:")
    print("\nPrice Categories Distribution:")
    print(df['price_category'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%')

    print("\nCountry of Origin Distribution:")
    print(df['country'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%')

    print("\nAverage Price by Country:")
    print(avg_price_by_country.round(2))

    print("\nBattery Statistics:")
    print(f"Average Battery Capacity: {df['battery_capacity'].mean():.0f} mAh")
    print(f"Average Battery Life: {df['battery_life'].mean():.0f} minutes")

def generate_detailed_summary(df, correlation_matrix, avg_price_by_country, rating_dist):
    """
    Generate a comprehensive analysis summary of the robot vacuum market.
    
    This function creates a detailed, structured report covering:
    - Market overview and price analysis
    - Manufacturer analysis
    - Technical specifications
    - Customer satisfaction
    - Key correlations
    - Market insights
    - Consumer recommendations
    
    The function needs the dataframe and results from previous analysis steps.
    It returns a list of text lines that make up the report, ready to be
    written to a file.
    """
    detailed_summary = [
        "\n\nDETAILED ANALYSIS SUMMARY",
        "=" * 40,
        
        "\n1. Market Overview and Price Analysis",
        "-" * 35,
        "• The robot vacuum market shows significant price diversity:",
        f"  - Price range spans from CHF {df['price'].min():.2f} to CHF {df['price'].max():.2f}",
        f"  - Average price: CHF {df['price'].mean():.2f}",
        f"  - Median price: CHF {df['price'].median():.2f}",
        "\n• Price Category Breakdown:",
        "\n".join(f"  - {category}: {count} models ({count/len(df)*100:.1f}%)" 
                 for category, count in df['price_category'].value_counts().items()),
        
        "\n2. Manufacturer Analysis",
        "-" * 35,
        f"• Total number of manufacturers: {df['manufacturer'].nunique()}",
        "\n• Top 5 Manufacturers by Market Share:",
        "\n".join(f"  - {mfr}: {count} models" 
                 for mfr, count in df['manufacturer'].value_counts().head().items()),
        
        "\n• Country of Origin Distribution:",
        "\n".join(f"  - {country}: {count} models ({count/len(df)*100:.1f}%)" 
                 for country, count in df['country'].value_counts().items()),
        
        "\n• Price Leadership by Country:",
        "\n".join(f"  - {country}: {price:.2f} CHF average" 
                 for country, price in avg_price_by_country.items()),
        
        "\n3. Technical Specifications",
        "-" * 35,
        "• Battery Performance:",
        f"  - Capacity Range: {df['battery_capacity'].min():.0f} - {df['battery_capacity'].max():.0f} mAh",
        f"  - Average Capacity: {df['battery_capacity'].mean():.0f} mAh",
        f"  - Average Battery Life: {df['battery_life'].mean():.0f} minutes",
        f"  - Average Charging Time: {df['charging_time'].mean():.0f} minutes",
        
        f"\n• Suction Power:",
        f"  - Range: {df['suction_power'].min():.0f} - {df['suction_power'].max():.0f} Pa",
        f"  - Average: {df['suction_power'].mean():.0f} Pa",
        
        "\n4. Customer Satisfaction",
        "-" * 35,
        f"• Overall Rating Statistics:",
        f"  - Average Rating: {df['rating'].mean():.2f} out of 5",
        f"  - Median Rating: {df['rating'].median():.2f}",
        "\n• Rating Distribution:",
        "\n".join(f"  - {label}: {count} models ({count/len(df)*100:.1f}%)" 
                 for label, count in rating_dist.items()),
        
        "\n5. Key Correlations",
        "-" * 35,
        "• Price Correlations:",
        f"  - Price vs Battery Capacity: {correlation_matrix.loc['price', 'battery_capacity']:.3f}",
        f"  - Price vs Battery Life: {correlation_matrix.loc['price', 'battery_life']:.3f}",
        f"  - Price vs Rating: {correlation_matrix.loc['price', 'rating']:.3f}",
        
        "\n6. Market Insights",
        "-" * 35,
        "• The mid-range segment dominates the market, suggesting strong competition in this price range",
        "• Chinese manufacturers have a significant market presence, particularly in the mid-range segment",
        "• South Korean brands command the highest average prices, suggesting premium positioning",
        "• Battery capacity shows a positive correlation with price, indicating it's a key factor in pricing",
        f"• {df['price_category'].value_counts().index[0]} is the most common price category, representing {df['price_category'].value_counts().iloc[0]/len(df)*100:.1f}% of the market",
        
        "\n7. Recommendations for Consumers",
        "-" * 35,
        "• Best value for money might be found in the mid-range segment (CHF 200-500)",
        "• Higher prices generally correlate with better battery performance",
        "• Consider Chinese brands for competitive pricing with good features",
        "• Premium features are most commonly found in South Korean and high-end Chinese models",
        "• Battery life and capacity should be key considerations in purchase decisions"
    ]
    
    return detailed_summary

def save_detailed_summary(detailed_summary, output_file='Vacuum robots info summary.txt'):
    """
    Save the detailed analysis summary to a text file.
    
    This function takes the list of text lines from generate_detailed_summary
    and writes them to a file, appending to any existing content.
    
    You can specify the output file path; by default it saves to
    'Vacuum robots info summary.txt'.
    """
    with open(output_file, 'a') as f:
        f.write('\n'.join(detailed_summary))
    
    print("\nDetailed summary has been added to the report file.")

def run_eda_analysis(input_file='robot_vacuums_cleaned.csv', plots_dir='plots', 
                    report_file='Vacuum robots info summary.txt'):
    """
    Run the complete EDA analysis pipeline in one go.
    
    This is the main function that ties everything together. It:
    1. Sets up visualization styles
    2. Creates the plots directory if needed
    3. Loads and processes the data
    4. Generates all visualizations
    5. Prints summary statistics
    6. Creates and saves a detailed report
    
    You can customize the input file, plots directory, and report file name.
    The function returns the processed dataframe for any further analysis
    you might want to do.
    """
    # Setup
    setup_visualization_style()
    ensure_plots_directory(plots_dir)
    
    # Load data
    df = pd.read_csv(input_file)
    
    # Add derived columns
    df = add_derived_columns(df)
    
    # Generate all plots
    plot_price_distribution(df, plots_dir)
    price_dist = plot_price_category_pie(df, plots_dir)
    country_dist = plot_country_distribution(df, plots_dir)
    plot_battery_vs_price(df, plots_dir)
    plot_battery_life_by_price(df, plots_dir)
    plot_price_battery_rating(df, plots_dir)
    avg_price_by_country = plot_avg_price_by_country(df, plots_dir)
    correlation_matrix = plot_correlation_matrix(df, plots_dir)
    
    # Get rating distribution
    rating_dist = df['rating_category'].value_counts()
    
    # Print summary statistics
    print_summary_statistics(df, price_dist, country_dist, avg_price_by_country)
    
    # Generate and save detailed summary
    detailed_summary = generate_detailed_summary(df, correlation_matrix, avg_price_by_country, rating_dist)
    save_detailed_summary(detailed_summary, report_file)
    
    print("\nPlots have been saved in the 'plots' directory.")
    
    return df

# If this script is run directly, perform the full analysis
if __name__ == "__main__":
    run_eda_analysis()






# function to run the different variants
def print_section(title):
    """Print a section title with separators for better readability"""
    print("\n" + "="*80)
    print(f" {title} ".center(78, "="))
    print("="*80 + "\n")


def eda_default_execution(input_df = 'robot_vacuums_cleaned.csv'):
    """
    This part of the script used Vacuum_EDA.py to plot some selected plots
    This script shows three different ways to use the Vacuum_EDA module:
    1. Default execution - Running the full EDA pipeline with default parameters
    """
    if not os.path.exists(input_df):
        print(f"Error: {input_df} not found. Please run clean_data.py first.")
        sys.exit(1)

    # EXAMPLE 1: Default execution - simplest way to run the full analysis
    print_section("EXAMPLE 1: Default Execution")
    print("Running the complete EDA analysis with default parameters...\n")
    print("This will:")
    print(" - Use 'robot_vacuums_cleaned.csv' as input")
    print(" - Save plots to the 'plots' directory")
    print(" - Append EDA results to 'Vacuum robots info summary.txt'")
    print("\nExecuting...\n")
    
    # Default execution
    run_eda_analysis()


def eda_custom_execution(input_df = 'robot_vacuums_cleaned.csv', custom_plots_dir = 'custom_plots', custom_report = 'Custom_EDA_Report.txt'):
    """
    This part of the script used Vacuum_EDA.py to plot some selected plots
    This script shows three different ways to use the Vacuum_EDA module:
    2. Custom execution - Specifying custom input, output files and plots directory
    """
    if not os.path.exists(input_df):
        print(f"Error: {input_df} not found. Please run clean_data.py first.")
        sys.exit(1)

    # EXAMPLE 2: Custom execution - specifying parameters
    print_section("EXAMPLE 2: Custom Execution")
    print("Running the EDA analysis with custom parameters...\n")
    
    # Create a custom plots directory
    print(f"This will:")
    print(f" - Use '{input_df}' as input")
    print(f" - Save plots to the '{custom_plots_dir}' directory")
    print(f" - Save report to '{custom_report}'")
    print("\nExecuting...\n")
    
    # Custom execution
    run_eda_analysis(
        input_file=input_df,
        plots_dir=custom_plots_dir,
        report_file=custom_report)
    
    
def eda_selective_execution(input_file = 'robot_vacuums_cleaned.csv', selective_plots_dir = 'selective_plots'):
    """
    This part of the script used Vacuum_EDA.py to plot some selected plots
    This script shows three different ways to use the Vacuum_EDA module:
    3. Selective execution - Running only specific analysis functions
    """
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Please run clean_data.py first.")
        sys.exit(1)
    
    # EXAMPLE 3: Selective execution - running only specific analyses
    print_section("EXAMPLE 3: Selective Execution")
    print("Running only selected analysis functions...\n")
    
    if not os.path.exists(selective_plots_dir):
        os.makedirs(selective_plots_dir)
    
    # Load and prepare data
    print("Loading and preparing data...")
    df = pd.read_csv(input_file)
    df_enriched = add_derived_columns(df)
    
    # Run selected analyses
    print("Generating selected plots:")
    print(" - Price distribution")
    plot_price_distribution(df_enriched, save_dir=selective_plots_dir)
    
    print(" - Country distribution")
    plot_country_distribution(df_enriched, save_dir=selective_plots_dir)
    
    print(" - Battery capacity vs price")
    plot_battery_vs_price(df_enriched, save_dir=selective_plots_dir)
    
    print(f"\nSelective plots have been saved to the '{selective_plots_dir}' directory.")