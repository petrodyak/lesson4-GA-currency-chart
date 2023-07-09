import requests
import uuid
import pygamp as pg
from decimal import Decimal


# Fetch the exchange rate from the National Bank of Ukraine API
response = requests.get(
    'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json')
exchange_data = response.json()
currency_rate = None


def send_event(currency_name, currency_rate,):
    label = 'UAH/' + currency_name
    # Send the UAH/USD ratio as a custom event to Google Analytics
    pg.event(
        cid='276331731',
        property_id='394362215',
        category='Currency',
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
        send_event (currency_name, currency_rate)
        continue


