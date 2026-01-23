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

def universe_column_configurations(lookback_period):
    '''
    Configure column styling for a streamlit DataFrame display
    Parameters:
        lookback_period: Period of historical data (str)
    Return:
        Column configuration (dict)
    '''

    # Format Lookback Period as Text
    time_dict = {'D': 'Day', 'M': 'Month', 'Y': 'Year'}
    if lookback_period == 'MAX':
        lookback_period_text = 'All Time'
    elif lookback_period == 'YTD':
        lookback_period_text = 'Year-to-Date'
    elif lookback_period[:-1] == '1':
        lookback_period_text = f'Last {time_dict[lookback_period[1]]}'
    else:
        lookback_period_text = f'Last {lookback_period[:-1]} {time_dict[lookback_period[-1]]}s'

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
            f'Prices ({lookback_period_text})',
            color = 'auto',
        )
    }

def macro_column_configurations():
    '''
    Configure column styling for a streamlit DataFrame display
    Parameters:
        None
    Return:
        Column configuration (dict)
    '''

    return {
        'Values': st.column_config.LineChartColumn(
            'Values (All Time)',
            color = '#F8F8F8',
            width = 'medium'
        )
    }