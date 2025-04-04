import pandas as pd
import numpy as np

"""
Robot Vacuum Data Cleaning and Analysis Utility

This module provides functions to clean, analyze, and create a short report on robot vacuum data.
It can be used as a standalone script or imported into other files to use its functions.
"""

def get_important_columns():
    """
    Returns the list of important columns to keep from the raw data.
    
    Returns:
        list: List of column names to keep
    """
    return [
        'product_name',
        'price',
        'rating',
        'rating_count',
        'Key specifications  Robot type',
        'Key specifications  Robot vacuum cleaner height i',
        'Key specifications  Battery life',
        'Key specifications  Max. noise level',
        'Key specifications  Robot vacuum cleaner features',
        'Key specifications  Smart home ecosystem',
        'General information  Manufacturer',
        'Robot vacuum cleaner properties  Max. Suction power i',
        'Robot vacuum cleaner properties  Filter + Dust bag volume',
        'Robot vacuum cleaner properties  Water tank capacity',
        'Robot vacuum cleaner properties  Suitable surfaces',
        'Robot vacuum cleaner properties  Max. Height door sill',
        'Robot vacuum cleaner properties  Room area i',
        'Battery properties  Battery life',
        'Battery properties  Charging time',
        'Battery properties  Battery type',
        'Battery properties  Capacity',
        'Colour  Colour',
        'Colour  Exact colour description',
        'Model  Model name',
        'Smart home features  Smart Home',
        'Product dimensions  Weight'
    ]

def get_column_rename_mapping():
    """
    Returns the mapping for renaming columns to more concise names.
    
    Returns:
        dict: Dictionary mapping original column names to new names
    """
    return {
        'Key specifications  Robot type': 'robot_type',
        'Key specifications  Robot vacuum cleaner height i': 'height',
        'Key specifications  Battery life': 'battery_life',
        'Key specifications  Max. noise level': 'noise_level',
        'Key specifications  Robot vacuum cleaner features': 'features',
        'Key specifications  Smart home ecosystem': 'smart_home_ecosystem',
        'General information  Manufacturer': 'manufacturer',
        'Robot vacuum cleaner properties  Max. Suction power i': 'suction_power',
        'Robot vacuum cleaner properties  Filter + Dust bag volume': 'dust_capacity',
        'Robot vacuum cleaner properties  Water tank capacity': 'water_capacity',
        'Robot vacuum cleaner properties  Suitable surfaces': 'suitable_surfaces',
        'Robot vacuum cleaner properties  Max. Height door sill': 'max_threshold',
        'Robot vacuum cleaner properties  Room area i': 'room_area',
        'Battery properties  Battery life': 'battery_life_spec',
        'Battery properties  Charging time': 'charging_time',
        'Battery properties  Battery type': 'battery_type',
        'Battery properties  Capacity': 'battery_capacity',
        'Colour  Colour': 'color_basic',
        'Colour  Exact colour description': 'color_exact'
    }

def get_price_corrections():
    """
    Returns known price corrections for specific products.
    
    Returns:
        dict: Dictionary mapping product names to corrected prices
    """
    return {
        'Samsung Jet Bot Combo AI Steam+ (VR9700)': 1440.05,  # Correcting decimal point error
        'Powerology Smart Robotic': 999.00,  # Correcting decimal point error
        'Neatron Robot hoover': 989.00,      # Correcting decimal point error
        'Aeco Vacubot X3': 979.50,           # Correcting decimal point error
        'Blaupunkt Vacuum cleaner - robot vacuum cleaner RVC201, White': 919.00,  # Correcting decimal point error
        'Severin RB7023 Robot Vacuum Cleaner Chill black / grey': 919.00         # Correcting decimal point error
    }

def get_battery_corrections():
    """
    Returns known battery capacity corrections for specific products.
    
    Returns:
        dict: Dictionary mapping product names to corrected battery capacities (in mAh)
    """
    return {
        'Mova P50 Pro Ultra': 5200,      # Correcting multiplier error
        'Liectroux V3SPro': 4400,        # Correcting multiplier error
        'Liectroux L200': 2600,          # Correcting multiplier error
    }

def validate_battery_capacity(capacity):
    """
    Validate and correct battery capacity if needed.
    
    Args:
        capacity: The battery capacity value to validate
        
    Returns:
        float: Validated and potentially corrected battery capacity, or np.nan if invalid
    """
    if pd.isna(capacity):
        return np.nan
    
    # Convert to float if string
    if isinstance(capacity, str):
        capacity = float(capacity.replace(',', ''))
    
    # Reasonable battery capacity range for robot vacuums (in mAh)
    MIN_CAPACITY = 1000   # Most robot vacuums have at least 1000 mAh
    MAX_CAPACITY = 10000  # Most high-end robot vacuums are under 10000 mAh
    
    if capacity > MAX_CAPACITY:
        # Check if it might be a multiplier error
        for divisor in [1000, 100, 10]:  # Try different divisors
            corrected_capacity = capacity / divisor
            if MIN_CAPACITY <= corrected_capacity <= MAX_CAPACITY:
                return corrected_capacity
    
    return capacity if MIN_CAPACITY <= capacity <= MAX_CAPACITY else np.nan

def extract_minutes(time_str):
    """
    Extract minutes from time strings in various formats.
    
    Args:
        time_str: String or numeric value representing time
        
    Returns:
        float: Extracted minutes as a float, or np.nan if invalid
    """
    if pd.isna(time_str):
        return np.nan
    if isinstance(time_str, (int, float)):
        return float(time_str)
    minutes = 0
    if 'min' in str(time_str):
        minutes = float(str(time_str).split('min')[0])
    return minutes

def clean_list_column(series):
    """
    Clean and convert comma-separated strings to lists.
    
    Args:
        series: Pandas series to clean
        
    Returns:
        Pandas series: Series with cleaned list values
    """
    # Convert to string, handle NaN values
    series = series.fillna('')
    # Split by comma and clean
    return series.str.split(',').apply(lambda x: [item.strip() for item in x if item.strip()])

def merge_colours(row):
    """
    Merge color information from two columns.
    
    Args:
        row: DataFrame row containing 'color_basic' and 'color_exact' columns
        
    Returns:
        str: Merged color information
    """
    color1 = row['color_basic']
    color2 = row['color_exact']
    
    # If either is NaN or empty, use the other one
    if pd.isna(color1) or color1 == '':
        return color2 if not pd.isna(color2) else ''
    if pd.isna(color2) or color2 == '':
        return color1
    # If they're the same, return either
    if color1 == color2:
        return color1
    # If they're different, combine them but avoid duplication
    colours = set(color1.split(', ') + color2.split(', '))
    return ', '.join(sorted(colours))

def validate_price(price):
    """
    Validate and correct price if needed.
    
    Args:
        price: The price value to validate
        
    Returns:
        float: Validated and potentially corrected price, or np.nan if invalid
    """
    if pd.isna(price):
        return np.nan
    
    # Convert to float if string
    if isinstance(price, str):
        price = float(price.replace(',', ''))
    
    # Reasonable price range for robot vacuums (in CHF)
    MIN_PRICE = 50
    MAX_PRICE = 3000  # Most high-end robot vacuums are under 3000 CHF
    
    if price > MAX_PRICE:
        # Check if it might be a decimal point error
        if price > 5000:  # Likely a decimal point error
            corrected_price = price / 10  # Try dividing by 10 first
            if MIN_PRICE <= corrected_price <= MAX_PRICE:
                return corrected_price
            
            corrected_price = price / 100  # Try dividing by 100 if still too high
            if MIN_PRICE <= corrected_price <= MAX_PRICE:
                return corrected_price
    
    return price if MIN_PRICE <= price <= MAX_PRICE else np.nan

def clean_data(input_file='robot_vacuums.csv', output_file='robot_vacuums_cleaned.csv', verbose=True):
    """
    Clean the robot vacuum data from a CSV file.
    
    Args:
        input_file (str): Path to the input CSV file
        output_file (str): Path to save the cleaned data
        verbose (bool): Whether to print status messages
        
    Returns:
        tuple: (original_df, cleaned_df) containing the original and cleaned DataFrames
    """
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Keep only the important columns
    important_columns = get_important_columns()
    df_cleaned = df[important_columns].copy()
    
    # Rename columns to be more concise
    column_rename = get_column_rename_mapping()
    df_cleaned = df_cleaned.rename(columns=column_rename)
    
    # Apply price corrections
    price_corrections = get_price_corrections()
    for product, correct_price in price_corrections.items():
        df_cleaned.loc[df_cleaned['product_name'] == product, 'price'] = correct_price
    
    # Clean numeric values
    # Remove 'dB' from noise level and convert to float
    df_cleaned['noise_level'] = df_cleaned['noise_level'].str.extract(r'(\d+\.?\d*)').astype(float)
    
    # Clean suction power (remove 'Pa' and convert to numeric)
    df_cleaned['suction_power'] = df_cleaned['suction_power'].str.extract(r'(\d+)').astype(float)
    
    # Clean room area (remove 'm²' and convert to numeric)
    df_cleaned['room_area'] = df_cleaned['room_area'].str.extract(r'(\d+)').astype(float)
    
    # Clean battery capacity (remove 'mAh' and convert to numeric)
    df_cleaned['battery_capacity'] = df_cleaned['battery_capacity'].str.extract(r'(\d+)').astype(float)
    
    # Apply battery corrections first
    battery_corrections = get_battery_corrections()
    for product, correct_capacity in battery_corrections.items():
        df_cleaned.loc[df_cleaned['product_name'] == product, 'battery_capacity'] = correct_capacity
    
    # Then apply general validation
    df_cleaned['battery_capacity'] = df_cleaned['battery_capacity'].apply(validate_battery_capacity)
    
    # Clean height values (remove 'cm' and convert to numeric)
    df_cleaned['height'] = df_cleaned['height'].str.extract(r'(\d+\.?\d*)').astype(float)
    df_cleaned['max_threshold'] = df_cleaned['max_threshold'].str.extract(r'(\d+)').astype(float)
    
    # Clean volume values (remove 'l' and convert to numeric)
    df_cleaned['dust_capacity'] = df_cleaned['dust_capacity'].str.extract(r'(\d+\.?\d*)').astype(float)
    df_cleaned['water_capacity'] = df_cleaned['water_capacity'].str.extract(r'(\d+\.?\d*)').astype(float)
    
    # Clean time values (extract minutes)
    df_cleaned['battery_life'] = df_cleaned['battery_life'].apply(extract_minutes)
    df_cleaned['battery_life_spec'] = df_cleaned['battery_life_spec'].apply(extract_minutes)
    df_cleaned['charging_time'] = df_cleaned['charging_time'].apply(extract_minutes)
    
    # Clean and convert to lists
    df_cleaned['suitable_surfaces'] = clean_list_column(df_cleaned['suitable_surfaces'])
    df_cleaned['features'] = clean_list_column(df_cleaned['features'])
    df_cleaned['smart_home_ecosystem'] = clean_list_column(df_cleaned['smart_home_ecosystem'])
    
    # Apply colour merging
    df_cleaned['color'] = df_cleaned.apply(merge_colours, axis=1)
    # Drop the original color columns
    df_cleaned = df_cleaned.drop(['color_basic', 'color_exact'], axis=1)
    
    # Apply price validation
    df_cleaned['price'] = df_cleaned['price'].apply(validate_price)
    
    # Remove rows with invalid prices
    df_cleaned = df_cleaned.dropna(subset=['price'])
    
    # Convert lists to strings for CSV storage
    df_to_save = df_cleaned.copy()
    df_to_save['suitable_surfaces'] = df_to_save['suitable_surfaces'].apply(lambda x: '|'.join(x) if x else '')
    df_to_save['features'] = df_to_save['features'].apply(lambda x: '|'.join(x) if x else '')
    df_to_save['smart_home_ecosystem'] = df_to_save['smart_home_ecosystem'].apply(lambda x: '|'.join(x) if x else '')
    
    # Drop duplicates
    df_to_save = df_to_save.drop_duplicates()
    
    # Reset index
    df_to_save = df_to_save.reset_index(drop=True)
    
    # Save cleaned data
    df_to_save.to_csv(output_file, index=False)
    
    if verbose:
        print("\nData completeness filtering:")
        print(f"Rows removed due to having more than 15 empty elements: {len(df) - len(df_cleaned)}")
        print(f"Rows remaining: {len(df_cleaned)}")
        
        print(f"\nData cleaning completed. Cleaned data saved to '{output_file}'")
        print(f"Original shape: {df.shape}")
        print(f"Cleaned shape: {df_to_save.shape}")
        
        # Print some statistics about the cleaned data
        print("\nData Statistics:")
        print(f"Number of unique manufacturers: {df_to_save['manufacturer'].nunique()}")
        print(f"Price range: ${df_to_save['price'].min():.2f} - ${df_to_save['price'].max():.2f}")
        print(f"Average rating: {df_to_save['rating'].mean():.2f}")
        print(f"Average battery life: {df_to_save['battery_life'].mean():.0f} minutes")
        print(f"Most common colours: {df_to_save['color'].value_counts().head(3).to_dict()}")
        print(f"Battery capacity range: {df_to_save['battery_capacity'].min():.0f} - {df_to_save['battery_capacity'].max():.0f} mAh")
    
    return df, df_to_save

def generate_report(df_cleaned, output_file='Vacuum robots info summary.txt', verbose=True):
    """
    Generate a comprehensive report about the cleaned robot vacuum data.
    
    Args:
        df_cleaned (DataFrame): Cleaned data DataFrame
        output_file (str): Path to save the report
        verbose (bool): Whether to print status messages
        
    Returns:
        list: List of report lines
    """
    if verbose:
        print("\nGenerating summary report...")
    
    # Initialize the report content
    report = []
    
    # Title
    report.append("VACUUM ROBOTS INFORMATION SUMMARY")
    report.append("=" * 40 + "\n")
    
    # Basic Statistics
    report.append("1. GENERAL OVERVIEW")
    report.append("-" * 20)
    report.append(f"Total number of robot models analyzed: {len(df_cleaned)}")
    report.append(f"Number of unique manufacturers: {df_cleaned['manufacturer'].nunique()}")
    report.append(f"Top 5 manufacturers by number of models:")
    top_manufacturers = df_cleaned['manufacturer'].value_counts().head(5)
    for mfr, count in top_manufacturers.items():
        report.append(f"  - {mfr}: {count} models")
    report.append("")
    
    # Price Analysis
    report.append("2. PRICE ANALYSIS")
    report.append("-" * 20)
    report.append(f"Price range: ${df_cleaned['price'].min():.2f} - ${df_cleaned['price'].max():.2f}")
    report.append(f"Average price: ${df_cleaned['price'].mean():.2f}")
    report.append(f"Median price: ${df_cleaned['price'].median():.2f}")
    report.append("\nPrice Categories:")
    price_bins = [0, 200, 500, 1000, float('inf')]
    price_labels = ['Budget (< $200)', 'Mid-range ($200-$500)', 'Premium ($500-$1000)', 'Luxury (> $1000)']
    df_cleaned['price_category'] = pd.cut(df_cleaned['price'], bins=price_bins, labels=price_labels)
    price_dist = df_cleaned['price_category'].value_counts()
    for category, count in price_dist.items():
        report.append(f"  - {category}: {count} models ({count/len(df_cleaned)*100:.1f}%)")
    report.append("")
    
    # Battery and Performance
    report.append("3. BATTERY AND PERFORMANCE")
    report.append("-" * 20)
    report.append(f"Battery Capacity Range: {df_cleaned['battery_capacity'].min():.0f} - {df_cleaned['battery_capacity'].max():.0f} mAh")
    report.append(f"Average Battery Life: {df_cleaned['battery_life'].mean():.0f} minutes")
    report.append(f"Average Charging Time: {df_cleaned['charging_time'].mean():.0f} minutes")
    report.append(f"Suction Power Range: {df_cleaned['suction_power'].min():.0f} - {df_cleaned['suction_power'].max():.0f} Pa")
    report.append("")
    
    # Features Analysis
    report.append("4. FEATURES ANALYSIS")
    report.append("-" * 20)
    # Convert string representation of lists back to actual lists
    features_df = df_cleaned.copy()
    features_df['features'] = features_df['features'].apply(lambda x: x.split('|') if isinstance(x, str) and x else [])
    all_features = [feature for features_list in features_df['features'] for feature in features_list]
    feature_counts = pd.Series(all_features).value_counts()
    report.append("Most Common Features:")
    for feature, count in feature_counts.head(10).items():
        report.append(f"  - {feature}: {count} models ({count/len(df_cleaned)*100:.1f}%)")
    report.append("")
    
    # Smart Home Integration
    report.append("5. SMART HOME INTEGRATION")
    report.append("-" * 20)
    features_df['smart_home_ecosystem'] = features_df['smart_home_ecosystem'].apply(lambda x: x.split('|') if isinstance(x, str) and x else [])
    all_ecosystems = [eco for eco_list in features_df['smart_home_ecosystem'] for eco in eco_list if eco]
    eco_counts = pd.Series(all_ecosystems).value_counts()
    report.append("Supported Smart Home Ecosystems:")
    for eco, count in eco_counts.items():
        report.append(f"  - {eco}: {count} models ({count/len(df_cleaned)*100:.1f}%)")
    report.append("")
    
    # Surface Compatibility
    report.append("6. SURFACE COMPATIBILITY")
    report.append("-" * 20)
    features_df['suitable_surfaces'] = features_df['suitable_surfaces'].apply(lambda x: x.split('|') if isinstance(x, str) and x else [])
    all_surfaces = [surface for surfaces_list in features_df['suitable_surfaces'] for surface in surfaces_list if surface]
    surface_counts = pd.Series(all_surfaces).value_counts()
    report.append("Compatible Surfaces:")
    for surface, count in surface_counts.head(10).items():
        report.append(f"  - {surface}: {count} models ({count/len(df_cleaned)*100:.1f}%)")
    report.append("")
    
    # Customer Satisfaction
    report.append("7. CUSTOMER SATISFACTION")
    report.append("-" * 20)
    report.append(f"Average Rating: {df_cleaned['rating'].mean():.2f} out of 5")
    rating_dist = pd.cut(df_cleaned['rating'], bins=[0, 3, 4, 4.5, 5], labels=['Below Average (< 3)', 'Good (3-4)', 'Very Good (4-4.5)', 'Excellent (4.5-5)'])
    rating_counts = rating_dist.value_counts()
    report.append("\nRating Distribution:")
    for rating, count in rating_counts.items():
        report.append(f"  - {rating}: {count} models ({count/len(df_cleaned)*100:.1f}%)")
    
    # Write the report to a file
    with open(output_file, 'w') as f:
        f.write('\n'.join(report))
    
    if verbose:
        print(f"Summary report has been created and saved as '{output_file}'")
    
    return report

def process_data(input_file='robot_vacuums.csv', 
                output_file='robot_vacuums_cleaned.csv', 
                report_file='Vacuum robots info summary.txt',
                verbose=True):
    """
    Processes the robot vacuum data: cleans it and generates a summary report.
    This is the main function to call from external scripts.
    
    Args:
        input_file (str): Path to the input CSV file
        output_file (str): Path to save the cleaned data
        report_file (str): Path to save the report
        verbose (bool): Whether to print status messages
        
    Returns:
        tuple: (original_df, cleaned_df, report) containing the original DataFrame, 
               cleaned DataFrame, and report lines
    """
    # Clean the data
    original_df, cleaned_df = clean_data(input_file, output_file, verbose)
    
    # Generate the report
    report = generate_report(cleaned_df, report_file, verbose)
    
    return original_df, cleaned_df, report

def get_cleaned_data(input_file='robot_vacuums.csv', force_clean=False):
    """
    Helper function to quickly get cleaned data without saving files.
    Useful for interactive analysis or when imported by other scripts.
    
    Args:
        input_file (str): Path to the input CSV file
        force_clean (bool): Whether to force cleaning even if cleaned file exists
        
    Returns:
        DataFrame: Cleaned data DataFrame
    """
    import os
    
    cleaned_file = 'robot_vacuums_cleaned.csv'
    
    # Check if cleaned file already exists
    if os.path.exists(cleaned_file) and not force_clean:
        return pd.read_csv(cleaned_file)
    else:
        # Clean data and return the cleaned DataFrame
        _, cleaned_df = clean_data(input_file, cleaned_file, verbose=False)
        return cleaned_df

# If this script is run directly, perform the full data processing
if __name__ == "__main__":
    # Run the entire data processing pipeline
    process_data(verbose=True) 