import yfinance as yf
import pandas as pd
import numpy as np

def get_ticker_data(ticker, lookback_period):
    '''
    Fetch relevant data for a stock
    Parameters:
        ticker: Ticker representing a stock (str)
        lookback_period: Amount of time to pull historical data (str)
    Returns:
        Price and fundamental data (dict)
    '''
    
    stock = yf.Ticker(ticker)
    
    # Format Lookback Period
    if lookback_period[1] == 'M':
        lookback_period += 'o'
    formatted_lookback = lookback_period.lower()

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
        'Prices': stock.history(period = formatted_lookback)['Close'].tolist()
    }

def get_universe_data(tickers, lookback_period):
    '''
    Fetch relevant data for a universe of stocks
    Parameters:
        ticker: Tickers representing a stock (list of str)
        lookback_period: Amount of time to pull historical data (str)
    Returns:
        Data for stocks (DataFrame)
    '''

    # Store Data
    universe_data = []

    # Pull Data for each Stock Individually
    for ticker in tickers:
        universe_data.append(get_ticker_data(ticker, lookback_period))
    
    # Convert to a DataFrame
    universe_df = pd.DataFrame(universe_data)
    universe_df.set_index('Ticker', inplace = True)
    return universe_df

def get_macro_data(indicator_codes, indicator_tickers, lookback_period):
    '''
    Fetch relevant macroeconomic data
    Parameters:
        indicator_codes: Codes representing an indicator provided by FRED (list of str)
        indicator_tickers: Tickers representing an ETF or index (list of str)
        lookback_period: Amount of time to pull historical data (str)
    Returns:
        Macroeconomic data (DataFrame)
    '''

    # Calculate start time

