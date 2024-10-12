import numpy as np
import pandas as pd
from faker import Faker

fake = Faker()

# Define product names for each category
product_names = {
    'Electronics': ['Smartphone', 'Laptop', 'Tablet', 'Headphones', 'Camera'],
    'Clothing': ['T-shirt', 'Jeans', 'Jacket', 'Dress', 'Sneakers'],
    'Grocery': ['Milk', 'Bread', 'Eggs', 'Fruits', 'Vegetables'],
    'Furniture': ['Chair', 'Table', 'Sofa', 'Bed', 'Bookshelf'],
    'Sports': ['Football', 'Basketball', 'Tennis Racket', 'Golf Club', 'Yoga Mat'],
    'Books': ['Novel', 'Biography', 'Comics', 'Cookbook', 'Textbook']
}

# Define a list of specific domain names
ecommerce_domains = ['Amazon', 'Flipkart', 'Myntra', 'eBay', 'Meesho']

# Define possible failure reasons
failure_reasons = {
    'card': ['Insufficient funds', 'Invalid card details', 'Card expired', 'Fraud suspected'],
    'Internet Banking': ['Payment gateway timeout', 'Exceeded transaction limit', 'Incorrect login credentials'],
    'UPI': ['Network issues', 'Incorrect UPI ID', 'Incorrect OTP'],
    'Wallet': ['Insufficient balance in wallet', 'Wallet account blocked', 'Wallet not authorized for transaction']
}

# Define specific countries and cities mapping
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

def generate_data(num_records, rogue_probability=0.05):
    data = []
    for _ in range(num_records):
        # Select a random product category
        product_category = fake.random_element(elements=list(product_names.keys()))
        
        # Select a random product name from the chosen category
        product_name = fake.random_element(elements=product_names[product_category])
        
        # Select a payment type
        payment_type = fake.random_element(elements=('card', 'Internet Banking', 'UPI', 'Wallet'))
        
        # Determine payment success or failure
        payment_success = fake.random_element(elements=('Y', 'N'))
        
        # Select a random country and corresponding city
        country = fake.random_element(elements=list(country_city_map.keys()))
        city = fake.random_element(elements=country_city_map[country])
        
        # Create a standard record
        record = {
            'order_id': fake.uuid4(),
            'customer_id': fake.uuid4(),
            'customer_name': fake.name(),
            'product_id': fake.uuid4(),
            'product_name': product_name,
            'product_category': product_category,
            'payment_type': payment_type,
            'qty': np.random.randint(1, 10),
            'price': round(np.random.uniform(10, 500), 2),
            'datetime': fake.date_time_this_decade(),
            'country': country,
            'city': city,
            'ecommerce_website_name': fake.random_element(elements=ecommerce_domains),
            'payment_txn_id': fake.uuid4(),
            'payment_txn_success': payment_success,
            'failure_reason': None
        }
        
        # Assign a failure reason if the payment is not successful
        if payment_success == 'N':
            record['failure_reason'] = fake.random_element(elements=failure_reasons[payment_type])
        
        # Introduce rogue records based on the probability
        if np.random.rand() < rogue_probability:
            # Alter some fields to introduce anomalies
            record['qty'] = np.random.choice([-1, 0, 1000])  # Invalid quantities
            record['price'] = np.random.choice([-100, 0])  # Invalid prices
            record['payment_type'] = 'Unknown'  # Invalid payment type
            record['country'] = 'Unknown'  # Invalid country
            record['city'] = 'Unknown'  # Invalid city
        
        data.append(record)
    
    return pd.DataFrame(data)

# Generate the data and save it to a CSV file
df = generate_data(10000)
df.to_csv('raw_generated_data.csv', index=False)
