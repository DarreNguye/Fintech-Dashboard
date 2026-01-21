import yfinance as yf
import pandas as pd
import numpy as np

def get_ticker_data(ticker, years):
    '''
    Fetch relevant data for a stock
    Parameters:
        ticker: Ticker representing a stock (str)
        years: Amount of years to pull historical data (int)
    Returns:
        Price and fundamental data (dict)
    '''
    
    stock = yf.Ticker(ticker)

    return {
        'Ticker': ticker,
        'Name': stock.info.get('shortName'),
        'Sector': stock.info.get('sector'),
        'Industry': stock.info.get('industry'),
        'Market Cap': stock.info.get('marketCap'),
        'Current Price': stock.info.get('currentPrice'),
        'Change ($)': stock.info.get('regularMarketChange'),
        'Change (%)': stock.info.get('regularMarketChangePercent') / 100,
        'Volume': stock.info.get('volume'),
        '52-wk Range': stock.info.get('fiftyTwoWeekRange'),
        'Prices': stock.history(period=f'{years}y')['Close'].tolist()
    }

def get_universe_data(tickers, years):
    '''
    Fetch relevant data for a universe of stocks
    Parameters:
        ticker: Tickers representing a stock (list of str)
        years: Amount of years to pull historical data (int)
    Returns:
        Data for stocks (DataFrame)
    '''

    # Store Data
    universe_data = []

    # Pull Data for each Stock Individually
    for ticker in tickers:
        universe_data.append(get_ticker_data(ticker, years))
    
    # Convert to a DataFrame
    universe_df = pd.DataFrame(universe_data)
    universe_df.set_index('Ticker', inplace = True)
    return universe_df