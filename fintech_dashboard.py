import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Page Setup
st.title('Fintech Dashboard')

# Sidebar for user input
st.sidebar.header('Configuration')
ticker = st.sidebar.text_input('Enter Ticker', value='NVDA').upper()
lookback_years = st.sidebar.slider('Lookback Period (Years)', 1, 5, 3)

# Fetch Data
def get_data(ticker, years):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=f'{years}y')
    info = stock.info
    return hist, info

# Load data
with st.spinner(f'Fetching data for {ticker}...'):
    try:
        df, info = get_data(ticker, lookback_years)
        
        # Metrics
        current_price = df['Close'].iloc[-1]
        prev_price = df['Close'].iloc[-2]
        daily_change = (current_price - prev_price) / prev_price * 100
        df['MA200'] = df['Close'].rolling(window=200).mean()
        df['StdDev'] = df['Close'].rolling(window=200).std()
        
        # Z-Score = (Price - Average) / Standard Deviation
        df['Z_Score'] = (df['Close'] - df['MA200']) / df['StdDev']
        latest_z = df['Z_Score'].iloc[-1]
        
        # Visualizations

        # Tickers
        col1, col2, col3, col4 = st.columns(4)
        col1.metric('Price', f"${current_price:.2f}", f"{daily_change:.2f}%")
        col2.metric('P/E Ratio', f"{info.get('forwardPE', 'N/A'):.1f}")
        col3.metric('Market Cap (in Billions)', f"${info.get('marketCap', 0)/1e9:.1f}")
        col4.metric('Valuation Z-Score', f"{latest_z:.2f}", 
                    help='Over 2.0 is expensive and under 2.0 is cheap')

        # Charts
        st.subheader(f'Price vs. 200-Day Average ({lookback_years} Years)')
        st.line_chart(df[['Close', 'MA200']])

        st.subheader('Valuation Heatmap (Z-Score)')
        st.write('When this chart spikes high, the stock is statistically extended.')
        st.bar_chart(df['Z_Score'])

    except Exception as e:
        st.error(f'Error fetching data for {ticker}')
        st.error(e)