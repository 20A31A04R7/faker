import pandas as pd

# Load the dataset
data = pd.read_csv('raw_generated_data.csv')
print(data)

# Display the data types and missing values
print(data.info())

# Check for duplicates
print(data.duplicated().sum())

#Define valid values for validation
valid_countries = {
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

valid_payment_types = ['Card', 'Internet Banking', 'UPI', 'Cash']
valid_payment_txn_success = ['Y', 'N']

data['invalid_qty'] = data['qty'] <= 0
data['invalid_price'] = data['price'] < 0
data['invalid_payment_type'] = ~data['payment_type'].isin(valid_payment_types)
data['invalid_country'] = ~data['country'].isin(valid_countries)
data['invalid_payment_txn_success'] = ~data['payment_txn_success'].isin(valid_payment_txn_success)

# Display rows with invalid quantities
invalid_qty_data = data[data['invalid_qty']]
if not invalid_qty_data.empty:
    print("Invalid Quantity (qty <= 0):")
    print(invalid_qty_data[['order_id', 'customer_id', 'qty']])
else:
    print("Invalid quantities not found.")

# Display rows with invalid prices
invalid_price_data = data[data['invalid_price']]
if not invalid_price_data.empty:
    print("\nInvalid Price (price < 0):")
    print(invalid_price_data[['order_id', 'customer_id', 'price']])
else:
    print("Invalid prices not found.")

# Display rows with invalid payment types
invalid_payment_type_data = data[data['invalid_payment_type']]
if not invalid_payment_type_data.empty:
    print("\nInvalid Payment Type (not in valid payment types):")
    print(invalid_payment_type_data[['order_id', 'customer_id', 'payment_type']])
else:
    print("Invalid payment types not found.")

# Display rows with invalid countries
invalid_country_data = data[data['invalid_country']]
if not invalid_country_data.empty:
    print("\nInvalid Country (not in valid countries):")
    print(invalid_country_data[['order_id', 'customer_id', 'country']])
else:
    print("Invalid countries not found.")
