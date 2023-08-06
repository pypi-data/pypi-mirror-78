from datetime import date, timedelta

import pandas as pd
from pandas_datareader import data as web


def get_target_date(base_date=date.today()):
    weekdays = [
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',
        'sunday',
    ]

    target_date = base_date
    weekday = weekdays[target_date.weekday()]
    if weekday == 'saturday':
        target_date = target_date - timedelta(days=1)
    elif weekday == 'sunday':
        target_date = target_date - timedelta(days=2)

    return target_date


def get_closing_price_from_yahoo(tickers, date):
    result = web.get_data_yahoo(tickers, date)
    return result['Adj Close']


def map_columns_without_suffix(tickers):
    return {ticker: ticker[:-3] for ticker in tickers}


def transpose_prices(prices):
    df = pd.DataFrame()
    df['symbol'] = prices.columns
    df['price'] = prices.values[0]
    df = df.round(2)
    return df


def calculate_multiplier(df, number_of_tickers, available_money):
    max_price = df['price'].max()
    percentage = 1 / number_of_tickers
    multiplier = (available_money * percentage) / max_price
    return multiplier


def calculate_amount(df, multiplier):
    return (df['price'].max()*multiplier/df['price']).round(0)


def calculate_total_for_each_ticker(df):
    return df['price']*df['amount']


def calculate_percentage_of_each_ticker(df):
    return df['total']/df['total'].sum() * 100
