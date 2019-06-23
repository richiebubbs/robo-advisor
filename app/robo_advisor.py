# app/robo_advisor.py
#create .env 
# I did need some help from the screencast found at: https://www.youtube.com/watch?v=UXAVOP1oCog&t=847s

import csv
import json
import os
import pandas as pd 
import matplotlib.pyplot as plt
import time


import statistics
from dotenv import load_dotenv
import requests
import datetime

#Here i am compiling a list of all stock symbols that I got from https://www.nasdaq.com/screening/company-list.aspx#
#I am using some of the dataframe skills I learned in Data Bootcamp with a little help from https://stackoverflow.com/questions/22341271/get-list-from-pandas-dataframe-column
#and https://stackoverflow.com/questions/23668427/pandas-three-way-joining-multiple-dataframes-on-columns

company_list_filepath = os.path.join(os.path.dirname(__file__), "..", "data", "companylist.csv")
company_list_2_filepath = os.path.join(os.path.dirname(__file__), "..", "data", "companylist_2.csv")
company_list_3_filepath = os.path.join(os.path.dirname(__file__), "..", "data", "companylist_3.csv")

df_1 = pd.read_csv(company_list_filepath)
df_2 = pd.read_csv(company_list_2_filepath)
df_3 = pd.read_csv(company_list_3_filepath)

valid_inputs = df_1["Symbol"].tolist() + df_2["Symbol"].tolist() + df_3["Symbol"].tolist()



#breakpoint()

load_dotenv()
def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

#INPUTS:

api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
#print(api_key)


a = False
while not a:
    symbol = input("Please select a stock symbol (e.g. MSFT) and press enter: ")
    if symbol not in valid_inputs:
        print("I'm sorry, that is not a valid entry please try again...")
        a = False
    else:
    
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
        price_data = pd.read_csv(csv_file_path)
        #print(price_data.columns)
        
        price_data_filtered = price_data["close"]

        # Here I am using standard deviation to measure volatility.  
        # A higher standard deviation would represent greater risk.  
        # I am using std between 0 and 5 to be defined as low risk
        # (essentially a standard deviation of x dollars signifies that 
        # 95% of the time the stock won't stray more than x dollars from its last closing price)
        # std >5-10 would be moderately risky
        # std over 10 is high risk
        # format help from https://stackoverflow.com/questions/455612/limiting-floats-to-two-decimal-points
        volatility = statistics.stdev(price_data_filtered)
        volatility_format = float("{0:.2f}".format(volatility))
        #print(volatility)
        
        
        
        print("-------------------------")
        print(f"SELECTED SYMBOL: {symbol}")
        print("-------------------------")
        print("REQUESTING STOCK MARKET DATA") 
        time.sleep(1)
        print("............................")
        time.sleep(1)
        print(f"REQUEST AT: {now}")
        print("-------------------------")
        print(f"LATEST DAY: {last_refreshed} ")
        print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
        print(f"RECENT HIGH: {to_usd(float(recent_high))}")
        print(f"RECENT LOW: {to_usd(float(recent_low))}")
        print("-------------------------")
        b = False
        while not b:
            risk_preference = input("What is your risk tolerance? Choose:(LOW, MODERATE, HIGH):  ")
            accepted_responses = ["LOW", "MODERATE", "HIGH"]
            if risk_preference not in accepted_responses:
                print("I'm sorry, I do not understand.  Please choose: LOW, MODERATE, HIGH - all caps, as it is case sensitive... ")
                b = False
            # I AM SURE THERE IS A MORE ELEGANT WAY TO WRITE THE FOLLOWING IN FEWER LINES USING A LOOPING FUNCTION, BUT THIS IS WHAT I HAVE...
            else:
                if risk_preference == "LOW" and volatility <5:
                    print("RECOMMENDATION: ")
                    time.sleep(1)
                    print("BUY!")
                    time.sleep(1)
                    print(f"RECOMMENDATION REASON: VOLATILITY = {volatility_format}, THIS IS A SAFE STOCK BASED ON YOUR RISK PREFERENCE")
                    time.sleep(1)
                elif risk_preference == "LOW" and volatility >5:
                    print("RECOMMENDATION: ")
                    time.sleep(1)
                    print("DO NOT BUY!")
                    time.sleep(1)
                    print(f"RECOMMENDATION REASON: VOLATILITY = {volatility_format}, THIS STOCK IS TOO RISKY BASED ON YOUR RISK PREFERENCE")
                    time.sleep(1)
                elif risk_preference == "MODERATE" and volatility <10 :
                    print("RECOMMENDATION: ")
                    time.sleep(1)
                    print("BUY!")
                    time.sleep(1)
                    print(f"RECOMMENDATION REASON: VOLATILITY = {volatility_format}, THIS IS A SAFE STOCK BASED ON YOUR RISK PREFERENCE")
                    time.sleep(1)
                elif risk_preference == "MODERATE" and volatility >10:
                    print("RECOMMENDATION: ")
                    time.sleep(1)
                    print("DO NOT BUY!")
                    time.sleep(1)
                    print(f"RECOMMENDATION REASON: VOLATILITY = {volatility_format}, THIS STOCK IS TOO RISKY BASED ON YOUR RISK PREFERENCE")
                    time.sleep(1)
                elif risk_preference == "HIGH" and volatility <5:
                    print("RECOMMENDATION: ")
                    time.sleep(1)
                    print("BUY FOR A SAFE INVESTMENT")
                    time.sleep(1)
                    print(f"RECOMMENDATION REASON: VOLATILITY = {volatility_format}, THIS STOCK IS A SAFE INVESTMENT, HOWEVER IT MAY NOT HAVE THE GROWTH POTENTIAL A RISK-TOLERANT INVESTOR LIKE YOU MAY BE LOOKING FOR")
                    time.sleep(1)
                elif risk_preference == "HIGH" and volatility >5 and volatility <10:
                    print("RECOMMENDATION: ")
                    time.sleep(1)
                    print("BUY!")
                    time.sleep(1)
                    print(f"RECOMMENDATION REASON: VOLATILITY = {volatility_format}, THIS IS A GOOD STOCK BASED ON YOUR RISK PREFERENCE WITH POTENTIAL GROWTH!")
                    time.sleep(1)
                elif risk_preference == "HIGH" and volatility >10:
                    print("RECOMMENDATION: ")
                    time.sleep(1)
                    print("BUY WITH CAUTION!")
                    time.sleep(1)
                    print(f"RECOMMENDATION REASON: VOLATILITY = {volatility_format}, THIS IS A GOOD STOCK BASED ON YOUR RISK PREFERENCE WITH POTENTIAL GROWTH, HOWEVER THE VOLATILITY IS HIGH, SO PROCEED WITH CAUTION!")
                    time.sleep(1)
                print("-------------------------")
                print(f"WRITING DATA TO CSV FILE: {csv_file_path}")
                print("-------------------------")
                print("HAPPY INVESTING!")
                print("-------------------------")
                time.sleep(1.5)
                print("WARNING: THIS APP IS A TOOL TO OFFER SOME LITTLE INSIGHT INTO THE STOCK MARKET, AND MAY NOT ADDRESS ALL OF YOUR INDIVIDUAL NEEDS.")
                print("PLEASE INVEST WISELY AND WITH HELP FROM A FINANCIAL ADVISOR")
                print("THE MAKERS OF THIS APP DO NOT GUARANTEE RETURNS, YOUR INVESTMENT IN THE STOCK MARKET MAY LOSE VALUE")
                b = True
       

        #price_data_filtered.plot()
        #plt.show()
        a = True
        b = True
        #print(price_data)


