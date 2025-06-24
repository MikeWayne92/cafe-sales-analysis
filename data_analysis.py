# Step 1: Import necessary libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Step 2: Load the data
# Load the CSV file into a Pandas DataFrame
file_path = 'dirty_cafe_sales.csv'
data = pd.read_csv(file_path)

# Step 3: Initial Inspection
# Display the first few rows of the dataset to understand its structure
print('Initial rows of the dataset:')
print(data.head())

# Step 4: Summary Statistics
# Generate a summary of the dataset to identify missing values and data types
print('\nSummary of the dataset:')
print(data.info())
print('\nMissing values in each column:')
print(data.isnull().sum())

# Step 5: Data Cleaning (Plan)
# Here, we will plan to handle missing values and correct data types
# This will be implemented in the next steps of the analysis
# For now, we just identify the issues

# Note: Further steps will include handling missing values, correcting data types,
# and performing exploratory data analysis (EDA) to uncover patterns and insights.

# Step 6: Data Cleaning

# Handle Missing Values
# Fill missing values with the mean of each numeric column
numeric_cols = data.select_dtypes(include=['number']).columns
data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())

# Correct Data Types
# Example: Convert date columns to datetime
data['Transaction Date'] = pd.to_datetime(data['Transaction Date'], errors='coerce')

# Address Inconsistencies
# Example: Standardize categorical values
# data['category_column'] = data['category_column'].str.lower()

# Replace non-numeric entries in 'Total Spent' with NaN
# This will allow us to handle them during data cleaning
data['Total Spent'] = pd.to_numeric(data['Total Spent'], errors='coerce')

# Option 1: Drop rows where 'Transaction Date' could not be parsed
data = data.dropna(subset=['Transaction Date'])

# Option 2: If you want to keep them, you can fill or flag them as needed
# data['Transaction Date'].fillna(method='ffill', inplace=True)  # Example: forward fill

# Proceed with the rest of the analysis

# Step 7: Exploratory Data Analysis (EDA)

# Visualize Data
# Example: Plot a histogram of a numerical column
plt.hist(data['Total Spent'], bins=20)
plt.title('Distribution of Total Spent')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()

# Note: Add more visualizations and analyses as needed to uncover patterns and insights.

# Ensure plots are displayed in a clean and organized manner
print(plt.style.available)

# Step 8: Sales Over Time

# Line Chart for total sales over time
# Assuming 'Transaction Date' is already converted to datetime
data['Transaction Date'] = pd.to_datetime(data['Transaction Date'])
data['Total Spent'] = pd.to_numeric(data['Total Spent'], errors='coerce')

daily_sales = data.groupby('Transaction Date')['Total Spent'].sum()
plt.figure(figsize=(12, 6))
plt.plot(daily_sales.index, daily_sales.values, marker='o')
plt.title('Total Sales Over Time')
plt.xlabel('Date')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Heatmap for sales by day of the week and hour
# Assuming 'Transaction Date' is already converted to datetime
data['Day of Week'] = data['Transaction Date'].dt.day_name()
data['Hour'] = data['Transaction Date'].dt.hour

heatmap_data = data.pivot_table(index='Day of Week', columns='Hour', values='Total Spent', aggfunc='sum')
plt.figure(figsize=(12, 6))
sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt='.0f')
plt.title('Sales Heatmap by Day of Week and Hour')
plt.xlabel('Hour of Day')
plt.ylabel('Day of Week')
plt.tight_layout()
plt.show()

# Step 9: Product Performance

# Bar Chart for total sales by product
product_sales = data.groupby('Item')['Total Spent'].sum().sort_values(ascending=False)
plt.figure(figsize=(12, 6))
product_sales.plot(kind='bar')
plt.title('Total Sales by Product')
plt.xlabel('Product')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Pie Chart for sales proportion by product category
plt.figure(figsize=(8, 8))
product_sales.plot(kind='pie', autopct='%1.1f%%')
plt.title('Sales Proportion by Product Category')
plt.ylabel('')
plt.tight_layout()
plt.show()

# Step 10: Payment Method Analysis

# Bar Chart for payment method frequency
payment_method_counts = data['Payment Method'].value_counts()
plt.figure(figsize=(10, 6))
payment_method_counts.plot(kind='bar')
plt.title('Payment Method Frequency')
plt.xlabel('Payment Method')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Step 11: Location-Based Insights

# Bar Chart for sales by location
location_sales = data.groupby('Location')['Total Spent'].sum().sort_values(ascending=False)
plt.figure(figsize=(12, 6))
location_sales.plot(kind='bar')
plt.title('Total Sales by Location')
plt.xlabel('Location')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Step 12: Customer Behavior

# Histogram for transaction amounts
plt.figure(figsize=(10, 6))
plt.hist(data['Total Spent'].dropna(), bins=20, color='skyblue', edgecolor='black')
plt.title('Distribution of Transaction Amounts')
plt.xlabel('Transaction Amount')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# Box Plot for sales amount distribution
plt.figure(figsize=(8, 6))
sns.boxplot(x=data['Total Spent'])
plt.title('Box Plot of Sales Amounts')
plt.xlabel('Sales Amount')
plt.tight_layout()
plt.show()

# Step 13: Correlation Analysis

# Scatter Plot for price per unit vs. quantity sold
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Price Per Unit', y='Quantity', data=data)
plt.title('Price Per Unit vs. Quantity Sold')
plt.xlabel('Price Per Unit')
plt.ylabel('Quantity Sold')
plt.tight_layout()
plt.show()

# Correlation Matrix for numerical variables
plt.figure(figsize=(10, 8))
corr_matrix = data.select_dtypes(include='number').corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix of Numerical Variables')
plt.tight_layout()
plt.show()

# Ensure plots are displayed in a clean and organized manner
print(plt.style.available)
