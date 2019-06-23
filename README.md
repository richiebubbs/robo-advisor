# robo-advisor

This app exists in the remote repository: https://github.com/richiebubbs/robo-advisor

To begin, fork the repository.
Use GitHub desktop to clone the repository to your computer's desktop.
Navigate to the app through the command line by using 
```sh
cd ~/Desktop/robo-advisor
```

## Create and Activate a virtual environment:

In the command line prompt, enter:

```sh
conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env
```

Also from the command line, install the required packages as follows:

```sh
pip install -r requirements.txt
pip install pytest # (only if you'll be writing tests)
```

To run the program from the command line:

```sh
python app/robo_advisor.py
```
# The App:

The app will prompt the user to enter a valid stock symbol,
for example, for microsoft, the user would enter MSFT

For a list of valid stock symbols consult: [List of Symbols](http://eoddata.com/symbols.aspx)

If the user enters an invalid symbol the app will return an error message and prompt the user to try again.

At this point the app will retrieve the pricing data for the selected stock, recent close, recent high, recent low and it will create a timestamp displaying when the request was made.

The app will then prompt the user to enter her risk tolerance level, LOW, MODERATE or HIGH.

Based on this information and the volatility of the stock (which was obtained by calculating the standard deviation of the historical closing prices) the app will issue a recommendation whether to Buy or Not Buy, with a brief explanation of the reasoning.

That's it, Happy Investing.

Remember this is just a simple app, so the recommendations are solely based on volatility.  Much more consideration should be used when making important financial decisions.  This app is not intended to be a true financial advisor, but rather an illustration of how to write code that simulates an advisor.  Please do not make any financial decisions without more comprehensive research and/or help from a financial advisor.

THANKS FOR CHECKING OUT MY APP!!




