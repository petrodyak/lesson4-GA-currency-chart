import requests
import time
import pygamp as pg
from decimal import Decimal


# Fetch the exchange rate from the National Bank of Ukraine API
response = requests.get(
    'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json')
exchange_data = response.json()
currency_rate = None
endpoint = 'https://www.google-analytics.com/mp/collect?api_secret=CYUIJF4wTheC4BXM3601-A&measurement_id=G-W979P61C5T'

def send_post_event (currency_name, currency_rate):
    label = 'UAH/' + currency_name
    payload = {
    'client_id': '276331731',  # Client ID (unique identifier for the user)
    'timestamp_micros': int(round(time.time() * 1000)), # Current milliseconds
    "session_id": "1456789",
    'events': [
        {
            'name': 'pd_currency_event',           
            "params":{
                "engagement_time_msec": "100",
                "session_id": "123",                
                'label': label, 
                'rate': currency_rate,
                "items":[
                        {'label': label, 'rate': currency_rate}
                ],
                "session_id":"1664435095", # Take custom ID from some site. TODO Get real name in my case
                "debug_mode":"1"
            }
        }
    ]
    }
    print ('payload:', payload)
    requests.post(endpoint, json=payload)

def send_event(currency_name, currency_rate):
    label = 'UAH/' + currency_name
    # Send the UAH/USD ratio as a custom event to Google Analytics
    pg.event(
        cid='276331731',
        property_id='394362215',
        category='Custom',
        action='Exchange Rate',
        label=label,
        value=currency_rate,
        non_interactive=0
    )
    # Confirm successful execution
    print(
        f'Successfully sent {currency_name}  exchange rate to Google Analytics: {currency_rate}')

for rate in exchange_data:
    currency_name = rate['cc']
    if currency_name in ('USD', 'EUR', 'PLN'):
        currency_rate = int(Decimal(rate['rate'])*10000) # convert into int due to Pygamp convert into int automatically 
        print(currency_name, ':', currency_rate)
        if currency_rate is None:
            # Handle error if exchange rate not found
            raise Exception(f'Unable to retrieve {currency_name} exchange rate.')
        # send_event (currency_name, currency_rate)
        send_post_event (currency_name, currency_rate)
        continue


