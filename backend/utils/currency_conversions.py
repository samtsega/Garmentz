import requests
from config import CURRENCY_API_KEY, BASE_CURRENCY
def get_conversion_rate(target_currency):
    """ Fetch the conversion rate from the base currency to the target currency using an external API.
    Args: target_currency (str): The currency code to convert to (e.g., 'EUR', 'GBP').
    Returns: float: Conversion rate from the base currency to the target currency. """

url = f"https://api.exchangeratesapi.io/latest?base={BASE_CURRENCY}&symbols={target_currency}"
try: response = requests.get(url, timeout=10) data = response.json()
if 'rates' in data and target_currency in data['rates']: return data['rates'][target_currency]
else: raise ValueError(f"Invalid response from currency API: {data}")
except requests.RequestException as e: print(f"Error fetching currency conversion rate: {e}")
return None

def convert_price(amount, target_currency):
""" Convert the price from the base currency to the target currency.
Args: amount (float): The amount in the base currency. target_currency (str): The currency code to convert to (e.g., 'EUR', 'GBP').
Returns: float: Converted price in the target currency. """

rate = get_conversion_rate(target_currency)
if rate: return round(amount * rate, 2)
else: raise Exception("Failed to fetch conversion rate.")

# Example usage:
if __name__ == "__main__": amount = 100 # Original amount in base currency
target_currency = 'EUR'
try: converted_price = convert_price(amount, target_currency)
print(f"{amount} {BASE_CURRENCY} is equal to {converted_price} {target_currency}")
except Exception as e: (
    print(f"Conversion failed: {e}"))