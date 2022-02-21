# Name: Ruben Sanduleac
# Date: 02/21/22
# Description: Stock News Alert notifies the user every morning about the
#              most relevant news info based on increase or decrease in stock.
#              The program uses Stock API from Alpha Vintage, News API for
#              newsapi.org, and twilio API to send text.

import requests
import os
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = os.environ["STOCK_API"]
NEWS_API_KEY = os.environ["NEWS_API"]
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
FROM_PHONE = os.environ["FROM_TEXT"]
TO_PHONE = os.environ["TO_TEXT"]

# pull the needed parameters from stock
parameters_stock = {}

# get a response from Stocks API
response_stock = requests.get(url=STOCK_ENDPOINT, params=parameters_stock)
response_stock.raise_for_status()
stock_data = response_stock.json()


# pull the needed parameters from news
parameters_news = {}

# get a response from Stocks API
response_news = requests.get(url=NEWS_ENDPOINT, params=parameters_news)
response_news.raise_for_status()
news_data = response_news.json()

