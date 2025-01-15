import pandas as pd

def get_customer_lifetime(customer_id):
    # Function to get the amount of time a customer has been active
    df = pd.read_csv('data/customer_lifetime.csv')
    customer_data = df[df['customer_id'] == customer_id]
    if not customer_data.empty:
        return customer_data['active_days'].values[0]
    else:
        return None

def get_customer_sales(customer_id, start_date=None, end_date=None):
    # Function to get the number of sales a customer has made in a given timeframe
    df = pd.read_csv('data/webshop_stats.csv')
    customer_data = df[df['customer_id'] == customer_id]
    if start_date:
        customer_data = customer_data[customer_data['date'] >= start_date]
    if end_date:
        customer_data = customer_data[customer_data['date'] <= end_date]
    return customer_data['sales'].sum()

def get_customer_revenue(customer_id, start_date=None, end_date=None, campaign_id=None):
    # Function to get the revenue (campaign spend) a customer has made in a given timeframe, optionally separated by campaign_id
    df = pd.read_csv('data/webshop_stats.csv')
    customer_data = df[df['customer_id'] == customer_id]
    if start_date:
        customer_data = customer_data[customer_data['date'] >= start_date]
    if end_date:
        customer_data = customer_data[customer_data['date'] <= end_date]
    if campaign_id:
        customer_data = customer_data[customer_data['campaign_id'] == campaign_id]
    return customer_data['revenue_euro'].sum()

def get_webshop_stats(customer_id):
    # Function to get the list of campaigns a customer has run
    df = pd.read_csv('data/webshop_stats.csv')
    customer_data = df[df['customer_id'] == customer_id]
    return list(set(list(customer_data['campaign_id'].tolist())))

AVAILABLE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_customer_lifetime",
            "description": """
                Get the amount of days a customer has been active.
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "number",
                        "description": "The ID of the customer."
                    }
                },
                "required": ["customer_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer_sales",
            "description": "Get the number of sales a customer has made in a given timeframe.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "number",
                        "description": "The ID of the customer."
                    },
                    "start_date": {
                        "type": "string",
                        "description": "The start date of the timeframe (optional)."
                    },
                    "end_date": {
                        "type": "string",
                        "description": "The end date of the timeframe (optional)."
                    }
                },
                "required": ["customer_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer_revenue",
            "description": "Get the revenue (campaign spend) a customer has made in a given timeframe, optionally separated by campaign_id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "number",
                        "description": "The ID of the customer."
                    },
                    "start_date": {
                        "type": "string",
                        "description": "The start date of the timeframe (optional)."
                    },
                    "end_date": {
                        "type": "string",
                        "description": "The end date of the timeframe (optional)."
                    },
                    "campaign_id": {
                        "type": "number",
                        "description": "The ID of the campaign (optional)."
                    }
                },
                "required": ["customer_id"]
            }
        }
    }
]