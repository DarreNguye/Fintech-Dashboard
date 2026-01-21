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