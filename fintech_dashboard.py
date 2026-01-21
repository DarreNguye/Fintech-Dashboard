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

# Load Data Frame
with st.spinner(f'Fetching data'):
    try:
       universe_column_configuration = styling.universe_column_configurations(lookback_years)
       
       # Stock DataFrame
       st.subheader('Stock Data')
       st.dataframe(
           styled_universe_df, 
           column_config = universe_column_configuration,
           width = 'stretch'
        )
       
       # Macros DataFrame
       st.subheader('Macros Data')

    except Exception as e:
        st.error(f'Error fetching data for {universe}')
        st.error(e)