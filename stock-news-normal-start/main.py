import requests
from twilio.rest import Client

import os
from dotenv import load_dotenv
from pathlib import Path
from twilio.rest import Client
import requests

# Load environment variables from .env
env_path = Path("..") / ".env"   # one directory up
load_dotenv(dotenv_path=env_path)

# Get them in Python
account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")
stock_api_key = os.getenv("STOCK_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_parameters = {
    "function":"TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "apikey": stock_api_key
}
response = requests.get("https://www.alphavantage.co/query", params=stock_parameters)
stock_data = response.json()
daily_data = stock_data["Time Series (Daily)"]
data_list = [value for (key, value) in daily_data.items()]
yday_data = data_list[0]
yday_closing_price = yday_data["4. close"]

day_before_yday_data = data_list[1]
day_before_yday_closing_price = day_before_yday_data["4. close"]

difference = float(yday_closing_price) - float(day_before_yday_closing_price)
up_down = None
if difference>0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((difference / float(yday_closing_price))*100)

if abs(diff_percent) > 0.0001:
    news_parameters = {
        "apikey": news_api_key,
        "qInTitle": COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    articles = news_response.json()["articles"]

    three_articles = articles[:3]
    print(three_articles)

    client = Client(account_sid, auth_token)

    headline_description = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    for article in three_articles:
        message = client.messages \
            .create(
            from_='whatsapp:+14155238886',
            body=headline_description,
            to="whatsapp:+16092401513"
        )


"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

