from decimal import Decimal, ROUND_DOWN

def convert_currency(amount, from_currency, to_currency, exchange_rates):
    """Convert between currencies using provided exchange rates"""
    if from_currency == to_currency:
        return amount
        
    # Convert via USD if no direct rate available
    usd_rate_from = exchange_rates.get(f"{from_currency}/USD")
    usd_rate_to = exchange_rates.get(f"{to_currency}/USD")
    
    if usd_rate_from and usd_rate_to:
        usd_amount = amount * usd_rate_from
        return usd_amount / usd_rate_to
        
    raise ValueError(f"No conversion rate available for {from_currency} to {to_currency}")

def format_currency(amount, currency="USD"):
    """Format currency amount with proper decimal places and symbol"""
    decimals = 8 if currency == "BTC" else 2
    symbol = "$" if currency == "USD" else currency
    
    formatted = f"{Decimal(amount).quantize(Decimal('1.' + '0'*decimals), rounding=ROUND_DOWN)}"
    return f"{symbol}{formatted}" if currency == "USD" else f"{formatted} {symbol}"