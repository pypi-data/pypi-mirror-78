from datetime import datetime

def current_datetime(utc=True):
    """
    returns the current utc time
    """
    formatter = '%Y-%m-%d %H:%M:%S.%f'
    if utc:
        return datetime.utcnow().strftime(formatter)
    return datetime.now().strftime(formatter)
