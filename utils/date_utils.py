from datetime import datetime, timedelta

def format_timestamp(ts, tz=None):
    """Format timestamp to human-readable string"""
    if isinstance(ts, (int, float)):
        dt = datetime.fromtimestamp(ts, tz=tz)
    else:
        dt = ts
        
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def relative_time(ts):
    """Convert timestamp to relative time string"""
    now = datetime.now()
    if isinstance(ts, (int, float)):
        dt = datetime.fromtimestamp(ts)
    else:
        dt = ts
        
    delta = now - dt
    
    if delta < timedelta(minutes=1):
        return "just now"
    elif delta < timedelta(hours=1):
        minutes = int(delta.seconds / 60)
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    elif delta < timedelta(days=1):
        hours = int(delta.seconds / 3600)
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    else:
        days = delta.days
        return f"{days} day{'s' if days > 1 else ''} ago"