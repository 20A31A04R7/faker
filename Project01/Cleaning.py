import numpy as np
import pandas as pd
from faker import Faker

fake = Faker()

# Define country-city mappings
country_city_map = {
    'USA': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
    'India': ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai'],
    'UK': ['London', 'Manchester', 'Birmingham', 'Liverpool', 'Leeds'],
    'Germany': ['Berlin', 'Munich', 'Frankfurt', 'Hamburg', 'Stuttgart'],
    'Canada': ['Toronto', 'Vancouver', 'Montreal', 'Calgary', 'Ottawa'],
    'Australia': ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide'],
    'France': ['Paris', 'Lyon', 'Marseille', 'Nice', 'Toulouse'],
    'Brazil': ['São Paulo', 'Rio de Janeiro', 'Brasilia', 'Salvador', 'Fortaleza'],
    'Japan': ['Tokyo', 'Osaka', 'Kyoto', 'Nagoya', 'Sapporo'],
    'South Africa': ['Johannesburg', 'Cape Town', 'Durban', 'Pretoria', 'Port Elizabeth']
}

# Define valid domains, payment types, and failure reasons
ecommerce_domains = ['Amazon', 'Flipkart', 'Myntra', 'eBay', 'Meesho']
valid_payment_types = ['card', 'Internet Banking', 'UPI', 'Wallet']
failure_reasons = {
    'card': ['Insufficient funds', 'Invalid card details', 'Card expired', 'Fraud suspected'],
    'Internet Banking': ['Payment gateway timeout', 'Exceeded transaction limit', 'Incorrect login credentials'],
    'UPI': ['Network issues', 'Incorrect UPI ID', 'Incorrect OTP'],
    'Wallet': ['Insufficient balance in wallet', 'Wallet account blocked', 'Wallet not authorized for transaction']
}

# Function to clean the schema
def clean_schema(df):
    df['qty'] = df['qty'].apply(lambda x: np.random.randint(1, 10) if pd.isnull(x) or x in [-1, 0, 1000] else x)
    df['price'] = df['price'].apply(lambda x: round(np.random.uniform(10, 500), 2) if pd.isnull(x) or x in [-100, 0] else x)
    df['payment_type'] = df['payment_type'].apply(lambda x: fake.random_element(elements=valid_payment_types) if pd.isnull(x) or x == 'Unknown' else x)

    # Assign country and corresponding city based on predefined list
    def assign_country_city(country, city):
        if pd.isnull(country) or country == 'Unknown':
            country = fake.random_element(elements=list(country_city_map.keys()))
        if pd.isnull(city) or city == 'Unknown':
            city = fake.random_element(elements=country_city_map[country])
        return country, city

    df[['country', 'city']] = df.apply(lambda row: assign_country_city(row['country'], row['city']), axis=1, result_type='expand')

    df['customer_name'] = df['customer_name'].apply(lambda x: fake.name() if pd.isnull(x) or not isinstance(x, str) or x.strip() == '' else x)
    df['ecommerce_website_name'] = df['ecommerce_website_name'].apply(lambda x: fake.random_element(elements=ecommerce_domains) if pd.isnull(x) or x not in ecommerce_domains else x)
    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce').fillna(fake.date_time_this_decade())

    # Fill missing 'failure_reason' with 'No Failure' when 'payment_txn_success' is 'Y'
    df['failure_reason'] = df['failure_reason'].fillna('No Failure')

    return df

# Function to load and clean data
def load_and_clean_data(input_file, output_file):
    df = pd.read_csv(input_file)
    df_cleaned = clean_schema(df)
    df_cleaned.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")

if __name__ == "__main__":
    # Example usage
    load_and_clean_data('generated_data.csv', 'ECommerce_generated_data.csv')
