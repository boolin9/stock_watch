import requests
import pandas as pd
import smtplib
import datetime


STOCK = "AAPL" # Pick any stock ticker symbol
COMPANY = 'Apple' 
TODAY_DATE = datetime.date.today()
MY_EMAIL = # Your email
PASSWORD =  # Your password
RECEIVER = # Recipient


API_KEY = # Alpha Vantage API key

parameters = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'interval': '60min',
    'apikey': API_KEY,
}

response = requests.get(url='https://www.alphavantage.co/query', params=parameters)
response.raise_for_status()

data = response.json()
stock_data = data['Time Series (Daily)']

today = list(stock_data.values())[0]
yesterday = list(stock_data.values())[1]

prices = [float(today['4. close']), float(yesterday['4. close'])]

price_series = pd.Series(prices)
perc_change = price_series.pct_change()[1]


API_KEY2 = # News API key

parameters2 = {
    'apiKey': API_KEY2,
    'q': COMPANY,
    'searchIn': 'title',
    'from': TODAY_DATE,
    'totalResults': 3,
    'language': 'en',
    'sortBy': 'popularity',
    'pageSize': 3,
    'page': 1,
}

response2 = requests.get(url='https://newsapi.org/v2/everything', params=parameters2)
response2.raise_for_status()

data = response2.json()
article_data = data['articles']

articles = [article_data[num] for num in range(3)]

if perc_change > 0.025 or perc_change < -0.025:
    if perc_change >= 0:
        symbol = '▲'
    else:
        symbol = '▼'

    subject = f'{STOCK}: {symbol} {round(perc_change, 3)}'

    message = f'''
    Source: {list(articles[0].values())[0]['name']}
    Brief: {list(articles[0].values())[3]}
    
    Source: {list(articles[1].values())[0]['name']}
    Brief: {list(articles[1].values())[3]}
    
    Source: {list(articles[2].values())[0]['name']}
    Brief: {list(articles[2].values())[3]}
    '''
    
    with smtplib.SMTP() as connection: # Add host
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=RECEIVER, msg=f"Subject:{subject}\n\n{message}".encode('utf-8'))