from datetime import datetime
import pytz


def to_date(date_str: str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def to_datetime(datetime_str: str):
    # Parse the ISO 8601 datetime string
    dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))

    # Check if the datetime object is naive (does not have timezone information)
    if dt.tzinfo is None:
        # Make the datetime object timezone aware
        dt = pytz.utc.localize(dt)
    else:
        # Convert the datetime object to UTC timezone
        dt = dt.astimezone(pytz.utc)

    # Convert to the desired time zone
    target_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    return dt.astimezone(target_tz)
