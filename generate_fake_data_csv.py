import os
import pandas as pd
import random
from datetime import datetime, timedelta

def generate_fake_customer_ids(num_customers=50):
    return random.sample(range(5000, 90001), num_customers)

def generate_customer_lifetime_csv(customer_ids, filename="customer_lifetime.csv"):
    data = {
        "customer_id": customer_ids,
        "active_days": [random.randint(1, 365) for _ in customer_ids]
    }
    df = pd.DataFrame(data)
    df.to_csv(os.path.join("data", filename), index=False)

def generate_webshop_stats_csv(customer_ids, lifetime_filename="customer_lifetime.csv", stats_filename="webshop_stats.csv"):
    # Read customer lifetime data
    lifetime_df = pd.read_csv(os.path.join("data", lifetime_filename))
    customer_lifetime = dict(zip(lifetime_df["customer_id"], lifetime_df["active_days"]))

    rows = []
    for customer_id in customer_ids:
        active_days = customer_lifetime[customer_id]
        max_start_day = 365 - active_days
        start_day = random.randint(0, max_start_day)
        start_date = datetime(2024, 1, 1) + timedelta(days=start_day)
        
        for i in range(active_days):
            date = start_date + timedelta(days=i)
            revenue_euro = round(random.uniform(100, 10000), 2)
            sales = random.randint(1, 100)
            rows.append([customer_id, date.strftime("%Y-%m-%d"), revenue_euro, sales])

    df = pd.DataFrame(rows, columns=["customer_id", "date", "revenue_euro", "sales"])
    df.to_csv(os.path.join("data", stats_filename), index=False)

# Example usage
customer_ids = generate_fake_customer_ids()
generate_customer_lifetime_csv(customer_ids)
generate_webshop_stats_csv(customer_ids)