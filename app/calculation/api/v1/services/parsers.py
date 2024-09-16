import re
from datetime import datetime


def parse_currency(value: str):
    """Extract numeric value from currency string."""
    return float(re.sub(r"[^\d.]+", "", value))


def parse_percentage(value: str):
    """Extract numeric value from percentage string."""
    return float(value.replace("%", "")) / 100


def parse_datetime(value: str):
    """Convert a string into a datetime object."""
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
