import requests
import csv
from datetime import datetime, timedelta

base_api_url = "https://services.bullionstar.com/spot-chart/getChart"

def fetch_data_from_api(api_params):
    response = requests.get(base_api_url, params=api_params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to fetch data from the API.")
        return None

def save_to_csv(gold_data, bitcoin_data, file_name):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Cost (USD)', 'Cost (Bitcoin)'])
        for entry_gold, entry_bitcoin in zip(gold_data['dataSeries'], bitcoin_data['dataSeries']):
            timestamp = int(gold_data['startDate']) + int(entry_gold['d'])
            date = datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
            gold_price_usd = entry_gold['v']
            bitcoin_price_usd = entry_bitcoin['v']
            writer.writerow([date, gold_price_usd, bitcoin_price_usd])

# Main function
def main():
    periods = ['DAY_1', 'WEEK_1', 'MONTH_1', 'YTD', 'YEAR_1', 'YEAR_3', 'MAX', 'CUSTOM']
    
    for period in periods:
        if period == 'CUSTOM':
            from_date = (datetime.now() - timedelta(days=365)).strftime('%d-%m-%Y %H:%M')
            to_date = datetime.now().strftime('%d-%m-%Y %H:%M')
        else:
            from_date = None
            to_date = None
        
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
        
        gold_data = fetch_data_from_api(api_params_gold)
        
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
        
        bitcoin_data = fetch_data_from_api(api_params_bitcoin)
        
        if gold_data and bitcoin_data:
            file_name = f'{period}.csv'
            save_to_csv(gold_data, bitcoin_data, file_name)
            print(f"Data saved to {file_name}")
        else:
            print("Failed to fetch data from the API.")

if __name__ == "__main__":
    main()
