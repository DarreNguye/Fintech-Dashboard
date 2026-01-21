import streamlit as st
import dashboard_data as data

# Page Setup
st.set_page_config(layout="wide")
st.title('Fintech Dashboard')

# Styling
def color_pos_or_neg(value):
    color = '#09AB3B' if value >= 0 else 'red'
    return f'color: {color};'

# Constants
universe = ['NVDA', 'AAPL', 'MSFT', 'AMZN', 'META', 'V', 'LULU']
lookback_years = 1
universe_df = data.get_universe_data(universe, lookback_years)
styled_universe_df = universe_df.style.map(color_pos_or_neg, subset=['Change (%)', 'Change ($)'])

# Configure Table
column_configuration = {
    'Market Cap': st.column_config.NumberColumn(
        'Market Cap',
        format = 'compact',
    ),

    'Current Price': st.column_config.NumberColumn(
        'Current Price',
        format = 'dollar',
    ),

    'Change ($)': st.column_config.NumberColumn(
        'Change ($)',
        format = 'dollar',
    ),

    'Change (%)': st.column_config.NumberColumn(
        'Change (%)',
        format = 'percent',
    ),

    'Volume': st.column_config.NumberColumn(
        'Volume',
        format = 'compact',
    ),

    'Prices': st.column_config.LineChartColumn(
        f'Prices (Last {lookback_years} years)',
        color = 'auto',
    )
}

# Load Data Frame
with st.spinner(f'Fetching data'):
    try:
       st.dataframe(
           styled_universe_df, 
           column_config = column_configuration,
           width = 'stretch'
        )
       st.dataframe(universe_df)

    except Exception as e:
        st.error(f'Error fetching data for {universe}')
        st.error(e)