import requests
import pandas as pd
from datetime import datetime, timedelta

# Define the base API endpoint
base_api_url = "https://services.bullionstar.com/spot-chart/getChart"

# Function to fetch data from the API
def fetch_data_from_api(api_params):
    response = requests.get(base_api_url, params=api_params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to fetch data from the API.")
        return None

# Main function to save data to CSV with multiple sheets
def save_to_csv(periods):
    with pd.ExcelWriter('scraping_data.xlsx') as writer:
        for period in periods:
            if period == 'CUSTOM':
                # Define the from and to dates for the custom period (from today's date last year to today's date)
                from_date = (datetime.now() - timedelta(days=365)).strftime('%d-%m-%Y %H:%M')
                to_date = datetime.now().strftime('%d-%m-%Y %H:%M')
            else:
                from_date = None
                to_date = None
            
            # Define API parameters for gold price data
            api_params_gold = {
                'product': 'false',
                'productId': '0',
                'productTo': 'false',
                'productIdTo': '0',
                'fromIndex': 'XAU',
                'toIndex': 'BTC',
                'period': period,
                'timeZoneId': 'Asia/Bangkok',
                'weightUnit': 'tr_oz'
            }
            
            if period == 'CUSTOM':
                api_params_gold['fromDateString'] = from_date
                api_params_gold['toDateString'] = to_date
            
            # Fetch gold price data from the API for the current period
            gold_data = fetch_data_from_api(api_params_gold)
            
            # Define API parameters for bitcoin price data
            api_params_bitcoin = {
                'product': 'false',
                'productId': '0',
                'productTo': 'false',
                'productIdTo': '0',
                'fromIndex': 'XAU',
                'toIndex': 'USD',
                'period': period,
                'timeZoneId': 'Asia/Bangkok',
                'weightUnit': 'tr_oz'
            }
            
            if period == 'CUSTOM':
                api_params_bitcoin['fromDateString'] = from_date
                api_params_bitcoin['toDateString'] = to_date
            
            # Fetch bitcoin price data from the API for the current period
            bitcoin_data = fetch_data_from_api(api_params_bitcoin)
            
            if gold_data and bitcoin_data:
                # Extract data from API response
                dates = []
                cost_usd = []
                cost_btc = []
                for entry_gold, entry_bitcoin in zip(gold_data['dataSeries'], bitcoin_data['dataSeries']):
                    timestamp = int(gold_data['startDate']) + int(entry_gold['d'])
                    date = datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
                    gold_price_usd = entry_gold['v']
                    bitcoin_price_usd = entry_bitcoin['v']
                    dates.append(date)
                    cost_usd.append(gold_price_usd)
                    cost_btc.append(bitcoin_price_usd)
                
                # Create DataFrame
                df = pd.DataFrame({'Date': dates, 'Cost (USD)': cost_usd, 'Cost (Bitcoin)': cost_btc})
                
                # Save DataFrame to Excel as a separate sheet
                df.to_excel(writer, sheet_name=period, index=False)

def main():
    periods = ['DAY_1', 'WEEK_1', 'MONTH_1', 'YTD', 'YEAR_1', 'YEAR_3', 'MAX', 'CUSTOM']
    save_to_csv(periods)

if __name__ == "__main__":
    main()
