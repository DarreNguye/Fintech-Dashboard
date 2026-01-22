import streamlit as st
import dashboard_data as data
import dashboard_styling as styling

# Page Setup
st.set_page_config(layout="wide")
st.title('Fintech Dashboard')

# Constants
universe = ['SOFI', 'AFRM', 'UPST', 'ENVA', 'LC', 'OPRT']

# Selection for Time Frame
period_options = ['1D', '5D', '1M', '6M', 'YTD', '1Y', '5Y', 'MAX']
lookback_period = st.segmented_control(
    'Period', period_options, default = '1Y'
)

# Load DataFrame
with st.spinner(f'Fetching data'):
    try:
       universe_df = data.get_universe_data(universe, lookback_period)
       styled_universe_df = universe_df.style.map(styling.color_pos_or_neg, subset=['Change (%)', 'Change ($)'])
       universe_column_configuration = styling.universe_column_configurations(lookback_period)
       
       # Stock DataFrame
       st.subheader('Stock Data')
       stock_table = st.dataframe(
           styled_universe_df, 
           column_config = universe_column_configuration,
           width = 'stretch'
        )
       
       # Macros DataFrame
       st.subheader('Macros Data')

    except Exception as e:
        st.error(f'Error fetching data for {universe}')
        st.error(e)