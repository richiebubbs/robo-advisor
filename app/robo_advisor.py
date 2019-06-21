# app/robo_advisor.py
#create .env 
# I did need some help from the screencast found at: https://www.youtube.com/watch?v=UXAVOP1oCog&t=847s

import csv
import json
import os
import pandas
import matplotlib.pyplot as plt



from dotenv import load_dotenv
import requests
import datetime


load_dotenv()
def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

#INPUTS:

api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
#print(api_key)

symbol = input("Please select a stock symbol (e.g. MSFT) and press enter: ")

request_url =f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
response = requests.get(request_url)
#print(type(response)) #<class 'requests.models.Response'>
#print(response.status_code) #200
#print(response.text)
now = datetime.datetime.now().replace(microsecond=0)
parsed_response = json.loads(response.text)
tsd = parsed_response["Time Series (Daily)"]
dates = list(tsd.keys())
latest_day = dates[0]
last_refreshed =  parsed_response['Meta Data']['3. Last Refreshed']
latest_close = parsed_response["Time Series (Daily)"][latest_day]["4. close"]
high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
csv_headers = ["timestamp", "open", "close", "volume"]


with open(csv_file_path, "w") as csv_file:
    
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader()
    for date in dates:    
        writer.writerow({
            "timestamp":date,
            "open":tsd[date]["1. open"],
            "close":tsd[date]["4. close"],
            "volume":tsd[date]["5. volume"]})

#print(high_prices)


#breakpoint()


#quit()



print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {now}")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed} ")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print(f"WRITING DATA TO CSV FILE: {csv_file_path}")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

price_data = pandas.read_csv(csv_file_path)


price_data.plot()
plt.show()

#print(price_data)


