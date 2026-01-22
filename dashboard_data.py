import yfinance as yf
import pandas as pd
import numpy as np
from fredapi import Fred

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

def calculate_start_date(lookback_period):
    '''
    Calculate a start date using the lookback_period
    Parameters:
        lookback_period: Amount of time to pull historical data (str)
    Returns:
        A start date (Timestamp)
    '''
    today = pd.Timestamp.now()

    # Handle MAX and YTD Lookback Periods
    if lookback_period == 'MAX':
        return None
    
    if lookback_period == 'YTD':
        return pd.to_datetime(today.replace(month = 1, day = 1))
    
    # Convert Look Back Period to Timestamp
    unit = lookback_period[-1]
    value = int(lookback_period[:-1])

    if unit == 'D':
        return pd.to_datetime(today - pd.DateOffset(days = value))
    elif unit == 'M':
        return pd.to_datetime(today - pd.DateOffset(months = value))
    elif unit == 'Y':
        return pd.to_datetime(today - pd.DateOffset(years = value))
    
    return None
    
def extend_series(series, start_date):
    '''
    Extend a series to a starting date and fill missing values with 0
    Parameters: 
        series: A series with a datetime index and no NaN values (Series)
        start_date: A time to extend the series to (Datetime)
    Returns:
        A series with an extended starting date (Series)
    '''

    # Create a Safe Copy
    extended_series = series.copy()

    # Add the start date if it is not in the series
    if start_date not in extended_series.index:
        extended_series.loc[start_date] = pd.NA  
        extended_series = extended_series.sort_index()

    # Resample to Daily
    extended_series = extended_series.resample('D').asfreq()

    # Fill NaN
    extended_series = extended_series.ffill().fillna(0)

    return extended_series
    

def get_macro_data(api_key, indicator_codes, lookback_period):
    '''
    Fetch relevant macroeconomic data
    Parameters:
        indicator_codes: Codes representing an indicator provided by FRED (dict)
        lookback_period: Amount of time to pull historical data (str)
    Returns:
        Macroeconomic data (DataFrame)
    '''

    # Calculate Start Date
    start_date = calculate_start_date(lookback_period)
    start_date_str = start_date.strftime('%Y-%m-%d') if start_date else None

    # Initialize FRED API
    fred = Fred(api_key = api_key)

    # Store Data
    macro_data = []

    # Pull Information for each Indicator
    for code in indicator_codes.keys():

        indicator_data = fred.get_series(code, observation_start = start_date_str)
        current_val = None if indicator_data.empty else indicator_data.iloc[-1]

        # Add Data
        macro_data.append({
            'Indicator': indicator_codes[code],
            'Code': code,
            'Current Value': current_val,
            'Values': indicator_data
        })

    # Convert to a DataFrame
    macro_df = pd.DataFrame(macro_data)
    macro_df.set_index('Indicator', inplace = True)
    return macro_df


