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
TARGET_DIFFERENCE = 5
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = os.environ["STOCK_API"]
NEWS_API_KEY = os.environ["NEWS_API"]
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
FROM_PHONE = os.environ["FROM_TEXT"]
TO_PHONE = os.environ["TO_TEXT"]

# pull the needed parameters from stock
parameters_stock = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "datatype": "json",
    "apikey": STOCK_API_KEY,
}

# get a response from Stocks API
response_stock = requests.get(url=STOCK_ENDPOINT, params=parameters_stock)
response_stock.raise_for_status()
stock_data = response_stock.json()["Time Series (Daily)"]


stock_data_list = [value for (key, value) in stock_data.items()]
yest_closing = float(stock_data_list[0]["4. close"])
day_before_yest_closing = float(stock_data_list[1]["4. close"])
difference_closing = abs(yest_closing - day_before_yest_closing)


percent_difference = round((difference_closing / day_before_yest_closing) * 100, 2)



# pull the needed parameters from news
parameters_news = {
    "apiKey": NEWS_API_KEY,
    "q": COMPANY_NAME,

}

# get a response from Stocks API
response_news = requests.get(url=NEWS_ENDPOINT, params=parameters_news)
response_news.raise_for_status()
news_data = response_news.json()["articles"][0:3]
news_list = [f"Headline: {articles['title']}. \n\nBrief: {articles['description']}\n\n" for articles in news_data]


def news_listings():
    total = ""
    for news in news_list:
        total += news

    return total


if percent_difference > TARGET_DIFFERENCE:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=f"{STOCK_NAME}:🔽{percent_difference}\n\n{news_listings()}",
        from_=FROM_PHONE,
        to=TO_PHONE
    )

else:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=f"{STOCK_NAME}:🔽{percent_difference}\n\n{news_listings()}",
        from_=FROM_PHONE,
        to=TO_PHONE
    )

# print the status once the text is sent.
print(message.status)
