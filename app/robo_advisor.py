# app/robo_advisor.py
#create .env 
# I did need some help from the screencast found at: https://www.youtube.com/watch?v=UXAVOP1oCog&t=847s

import requests
import json
import datetime

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

#INPUTS:
request_url ="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"
response = requests.get(request_url)
#print(type(response)) #<class 'requests.models.Response'>
#print(response.status_code) #200
#print(response.text)

parsed_response = json.loads(response.text)
last_refreshed =  parsed_response['Meta Data']['3. Last Refreshed']
latest_close = parsed_response["Time Series (Daily)"]["2019-06-18"]["4. close"]



#breakpoint()


#quit()



print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed} ")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")