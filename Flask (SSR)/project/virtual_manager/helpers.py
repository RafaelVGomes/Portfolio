def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

def percent_diff(current_value, previous_value):
    """Format difference of values to [-]0.00%"""
    return round(float((current_value / previous_value - 1) * 100), 2)
