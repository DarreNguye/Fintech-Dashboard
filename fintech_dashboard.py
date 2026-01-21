import streamlit as st
import dashboard_data as data
import dashboard_styling as styling

# Page Setup
st.set_page_config(layout="wide")
st.title('Fintech Dashboard')

# Constants
universe = ['SOFI', 'AFRM', 'UPST', 'ENVA', 'LC', 'OPRT']
lookback_years = 1
universe_df = data.get_universe_data(universe, lookback_years)
styled_universe_df = universe_df.style.map(styling.color_pos_or_neg, subset=['Change (%)', 'Change ($)'])

# Configure DataFrame
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

    except Exception as e:
        st.error(f'Error fetching data for {universe}')
        st.error(e)