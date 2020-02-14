import os
from finnhub import FinnHub
from datapackage import Package
from tqdm import tqdm
import json
from datetime import datetime

import schedule 
import time

def get_token(filepath): 
    with open(os.path.abspath(filepath)) as f:
        data = f.readlines()
        f.close()
    return data[0]

def main():
    now = datetime.now()
    string = now.strftime('%m-%d-%Y')
    token = get_token('./token.txt')
    package = Package('https://datahub.io/core/s-and-p-500-companies/datapackage.json')
    sp500companies = package.get_resource('constituents').read()
    sp500_stock_data = []

    for company in tqdm(sp500companies): 
        symbol = company[0]
        finn_symbol = FinnHub(symbol, token)
        sp500_stock_data.append(finn_symbol.stock_data())
    
    if not os.path.exists('./stock_data'):
        os.makedirs('./stock_data')
    
    with open('./stock_data/run_{}.json'.format(string), 'w') as f:
        json.dump(sp500_stock_data, f, indent=4)
        f.close()
        
    


if __name__ == "__main__":
    schedule.every().day.at('01:00').do(main)

    while True:
        schedule.run_pending()
        time.sleep(60)