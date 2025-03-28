import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Read the cleaned data
df = pd.read_csv('robot_vacuums_cleaned.csv')

# Create a directory for saving plots if it doesn't exist
import os
if not os.path.exists('plots'):
    os.makedirs('plots')

# 1. Price Distribution Analysis
plt.figure(figsize=(12, 6))
sns.histplot(data=df, x='price', bins=30, kde=True)
plt.title('Distribution of Robot Vacuum Prices')
plt.xlabel('Price (CHF)')
plt.ylabel('Count')
# Add mean and median lines
plt.axvline(df['price'].mean(), color='red', linestyle='--', label=f'Mean: CHF {df["price"].mean():.2f}')
plt.axvline(df['price'].median(), color='green', linestyle='--', label=f'Median: CHF {df["price"].median():.2f}')
plt.legend()
plt.savefig('plots/price_distribution.png')
plt.close()

# Create price categories for further analysis
price_bins = [0, 200, 500, 1000, float('inf')]
price_labels = ['Budget (< CHF 200)', 'Mid-range (CHF 200-500)', 'Premium (CHF 500-1000)', 'Luxury (> CHF 1000)']
df['price_category'] = pd.cut(df['price'], bins=price_bins, labels=price_labels)

# Price category distribution
plt.figure(figsize=(10, 6))
price_dist = df['price_category'].value_counts()
plt.pie(price_dist, labels=price_dist.index, autopct='%1.1f%%', startangle=90)
plt.title('Distribution of Robot Vacuums by Price Category')
plt.axis('equal')
plt.savefig('plots/price_category_pie.png')
plt.close()

# 2. Manufacturer Country Analysis
# Extract country information from manufacturer names and known brands
def get_country(manufacturer):
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

df['country'] = df['manufacturer'].apply(get_country)

# Create pie chart for country distribution
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

plt.savefig('plots/country_distribution.png', bbox_inches='tight', dpi=300)
plt.close()

# 3. Battery Analysis
# Battery Capacity vs Price
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
plt.savefig('plots/battery_vs_price.png')
plt.close()

# Battery Life Distribution by Price Category
plt.figure(figsize=(12, 6))
sns.boxplot(data=df[df['battery_life'] <= 500], x='price_category', y='battery_life')
plt.title('Battery Life Distribution by Price Category\n(Showing robots with battery life ≤ 500 minutes)', pad=20)
plt.xlabel('Price Category', labelpad=10)
plt.ylabel('Battery Life (minutes)', labelpad=10)
plt.ylim(0, 500)  # Set y-axis limits
plt.grid(True, alpha=0.3)  # Add light grid
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('plots/battery_life_by_price.png', bbox_inches='tight', dpi=300)
plt.close()

# 4. Combined Analysis: Price, Battery, and Rating
fig = plt.figure(figsize=(12, 8))
scatter = plt.scatter(df['battery_capacity'], df['price'], 
                     c=df['rating'], cmap='viridis', 
                     alpha=0.6, s=100)
plt.colorbar(scatter, label='Rating')
plt.title('Price vs Battery Capacity (colored by Rating)')
plt.xlabel('Battery Capacity (mAh)')
plt.ylabel('Price (CHF)')
plt.tight_layout()
plt.savefig('plots/price_battery_rating.png')
plt.close()

# 5. Average Price by Country
plt.figure(figsize=(10, 6))
avg_price_by_country = df.groupby('country')['price'].mean().sort_values(ascending=False)
avg_price_by_country.plot(kind='bar')
plt.title('Average Price by Country of Origin')
plt.xlabel('Country')
plt.ylabel('Average Price (CHF)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('plots/avg_price_by_country.png')
plt.close()

# Print summary statistics
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

# Save correlation matrix
correlation_matrix = df[['price', 'battery_capacity', 'battery_life', 'rating']].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix')
plt.tight_layout()
plt.savefig('plots/correlation_matrix.png')
plt.close()

# Calculate rating distribution
rating_bins = [0, 3, 4, 4.5, 5]
rating_labels = ['Below Average (< 3)', 'Good (3-4)', 'Very Good (4-4.5)', 'Excellent (4.5-5)']
df['rating_category'] = pd.cut(df['rating'], bins=rating_bins, labels=rating_labels)
rating_dist = df['rating_category'].value_counts()

# Generate detailed summary
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

# Append the detailed summary to the existing report file
with open('Vacuum robots info summary.txt', 'a') as f:
    f.write('\n'.join(detailed_summary))

print("\nDetailed summary has been added to the report file.")

print("\nPlots have been saved in the 'plots' directory.") 