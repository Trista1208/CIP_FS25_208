import pandas as pd
import numpy as np

# Read the CSV file
df = pd.read_csv('robot_vacuums.csv')

# List of important columns to keep
important_columns = [
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
    'Colour  Exact colour description'
]

# Keep only the important columns
df_cleaned = df[important_columns].copy()

# Rename columns to be more concise
column_rename = {
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
    'Colour  Colour': 'Colour Colour',
    'Colour  Exact colour description': 'colour_exact'
}
df_cleaned = df_cleaned.rename(columns=column_rename)

# Merge color columns
def merge_colours(row):
    # If exact colour is NaN or empty, use the basic colour
    if pd.isna(row['colour_exact']) or row['colour_exact'] == '':
        return row['Colour Colour']
    # If basic colour is NaN or empty, use the exact colour
    if pd.isna(row['Colour Colour']) or row['Colour Colour'] == '':
        return row['colour_exact']
    # If they're the same, return either
    if row['Colour Colour'] == row['colour_exact']:
        return row['Colour Colour']
    # If they're different, combine them but avoid duplication
    colours = set(row['Colour Colour'].split(', ') + row['colour_exact'].split(', '))
    return ', '.join(sorted(colours))

# Apply colour merging
df_cleaned['Colour Colour'] = df_cleaned.apply(merge_colours, axis=1)
# Drop the exact colour column
df_cleaned = df_cleaned.drop('colour_exact', axis=1)

# Clean numeric values
# Remove 'dB' from noise level and convert to float
df_cleaned['noise_level'] = df_cleaned['noise_level'].str.extract('(\d+\.?\d*)').astype(float)

# Clean suction power (remove 'Pa' and convert to numeric)
df_cleaned['suction_power'] = df_cleaned['suction_power'].str.extract('(\d+)').astype(float)

# Clean room area (remove 'm²' and convert to numeric)
df_cleaned['room_area'] = df_cleaned['room_area'].str.extract('(\d+)').astype(float)

# Clean battery capacity (remove 'mAh' and convert to numeric)
df_cleaned['battery_capacity'] = df_cleaned['battery_capacity'].str.extract('(\d+)').astype(float)

# Clean time values (extract minutes)
def extract_minutes(time_str):
    if pd.isna(time_str):
        return np.nan
    if isinstance(time_str, (int, float)):
        return float(time_str)
    minutes = 0
    if 'min' in str(time_str):
        minutes = float(str(time_str).split('min')[0])
    return minutes

df_cleaned['battery_life'] = df_cleaned['battery_life'].apply(extract_minutes)
df_cleaned['battery_life_spec'] = df_cleaned['battery_life_spec'].apply(extract_minutes)
df_cleaned['charging_time'] = df_cleaned['charging_time'].apply(extract_minutes)

# Clean height values (remove 'cm' and convert to numeric)
df_cleaned['height'] = df_cleaned['height'].str.extract('(\d+\.?\d*)').astype(float)
df_cleaned['max_threshold'] = df_cleaned['max_threshold'].str.extract('(\d+)').astype(float)

# Clean volume values (remove 'l' and convert to numeric)
df_cleaned['dust_capacity'] = df_cleaned['dust_capacity'].str.extract('(\d+\.?\d*)').astype(float)
df_cleaned['water_capacity'] = df_cleaned['water_capacity'].str.extract('(\d+\.?\d*)').astype(float)

# Process list-like columns
def clean_list_column(series):
    # Convert to string, handle NaN values
    series = series.fillna('')
    # Split by comma and clean
    return series.str.split(',').apply(lambda x: [item.strip() for item in x if item.strip()])

# Clean and convert to lists
df_cleaned['suitable_surfaces'] = clean_list_column(df_cleaned['suitable_surfaces'])
df_cleaned['features'] = clean_list_column(df_cleaned['features'])
df_cleaned['smart_home_ecosystem'] = clean_list_column(df_cleaned['smart_home_ecosystem'])
df_cleaned['Colour Colour'] = clean_list_column(df_cleaned['Colour Colour'])

# Convert lists to strings for CSV storage
df_to_save = df_cleaned.copy()
df_to_save['suitable_surfaces'] = df_to_save['suitable_surfaces'].apply(lambda x: '|'.join(x) if x else '')
df_to_save['features'] = df_to_save['features'].apply(lambda x: '|'.join(x) if x else '')
df_to_save['smart_home_ecosystem'] = df_to_save['smart_home_ecosystem'].apply(lambda x: '|'.join(x) if x else '')
df_to_save['Colour Colour'] = df_to_save['Colour Colour'].apply(lambda x: '|'.join(x) if x else '')

# Drop duplicates
df_to_save = df_to_save.drop_duplicates()

# Reset index
df_to_save = df_to_save.reset_index(drop=True)

# Save cleaned data
df_to_save.to_csv('robot_vacuums_cleaned.csv', index=False)

print("Data cleaning completed. Cleaned data saved to 'robot_vacuums_cleaned.csv'")
print(f"Original shape: {df.shape}")
print(f"Cleaned shape: {df_to_save.shape}")

# Print some statistics about the cleaned data
print("\nData Statistics:")
print(f"Number of unique manufacturers: {df_to_save['manufacturer'].nunique()}")
print(f"Price range: ${df_to_save['price'].min():.2f} - ${df_to_save['price'].max():.2f}")
print(f"Average rating: {df_to_save['rating'].mean():.2f}")
print(f"Average battery life: {df_to_save['battery_life'].mean():.0f} minutes")
print(f"Most common colours: {df_to_save['Colour Colour'].value_counts().head(3).to_dict()}") 