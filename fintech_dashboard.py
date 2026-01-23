import streamlit as st
import dashboard_data as data
import dashboard_styling as styling
from dotenv import load_dotenv
import os

# Page Setup
st.set_page_config(layout="wide")
st.title('Fintech Dashboard')

# Load .env Variables
load_dotenv()

# Constants
fred_api_key = os.getenv('FRED_API_KEY')
universe = ['SOFI', 'AFRM', 'UPST', 'ENVA', 'LC', 'OPRT']
period_options = ['1D', '5D', '1M', '6M', 'YTD', '1Y', '5Y', 'MAX']
indicators = {
    'UNRATE': 'Unemployment', 
    'DFF': 'Interest', 
    'DRCCLACBS': 'Credit Card Delinquency',
    'DROCLACBS': 'Other Consumer Delinquency',
    'PSAVERT': 'Personal Savings'
    }

# Load Stock Data
st.subheader('Stock Data')
with st.spinner(f'Fetching data'):
    try:
        # Selection for Time Frame
        stock_lookback_period = st.segmented_control(
            'Period', period_options, default = '1Y', key = 'stock'
        )
        
        # Get Data and Configs
        universe_df = data.get_universe_data(universe, stock_lookback_period)
        styled_universe_df = universe_df.style.map(styling.color_pos_or_neg, subset=['Change (%)', 'Change ($)'])
        universe_column_configuration = styling.universe_column_configurations(stock_lookback_period)
        
        # Stock DataFrame
        stock_table = st.dataframe(
           styled_universe_df, 
           column_config = universe_column_configuration,
           width = 'stretch'
        )

    except Exception as e:
        st.error(f'Error fetching stock data')
        st.error(e)

# Load Macro Data
st.subheader('Macro Data')
with st.spinner(f'Fetching data'):
    try:
        # Get Data and Configs
        macro_df = data.get_macro_data(fred_api_key, indicators)
        macro_column_configuration = styling.macro_column_configurations()
        
        # Macro DataFrame
        macro_table = st.dataframe(
           macro_df, 
           column_config = macro_column_configuration,
           width = 'content'
        )

    except Exception as e:
        st.error(f'Error fetching macro data')
        st.error(e)
