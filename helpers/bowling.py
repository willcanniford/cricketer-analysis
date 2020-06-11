import re


def total_balls(overs_str, str_ignore=['DNB'], ignore_value=0):
    '''
    Calculate total balls bowled from overs formatting

    Parameters
    ----------
    overs_str: string
        Overs bowled in traditional format overs.balls
    str_ignore: list
        Strings to ignore and return 0 - indicators that the player didn't bowl
    ignore_value: int
        Value to input for strings matched into str_ignore
        
    Returns 
    ------- 
    int:
        The number of balls bowled as an int 
    '''
    if overs_str in str_ignore:
        return(ignore_value)

    grouping_re = re.compile(r'^([0-9]*)\.([0-5]*)$').search(overs_str)

    if grouping_re is None:
        return(int(overs_str) * 6)
    else:
        overs = int(grouping_re.group(1)) * 6
        balls = int(grouping_re.group(2))
        return(overs + balls)
