import streamlit as st

def color_pos_or_neg(value):
    '''
    Classify percent changes as positive or negative and assign a color
    Parameters:
        value: percentage to classify (float)
    Return:
        Green (positive) or red (negative) (str)
    '''

    color = '#09AB3B' if value >= 0 else 'red'
    return f'color: {color};'

def universe_column_configurations(lookback_years):
    '''
    Configure column styling for a streamlit DataFrame display
    Parameters:
        lookback_years: Years of historical data (int)
    Return:
        Column configuration (dict)
    '''

    return {
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