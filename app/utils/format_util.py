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


def to_date_time_full_format(date: datetime):
    hours = date.hour
    minutes = str(date.minute).zfill(2)  # Sử dụng zfill để thêm số 0 vào đầu nếu cần

    am_pm = 'PM' if hours >= 12 else 'AM'
    hours = hours % 12 or 12  # Đặt giờ thành 12 nếu là 0

    day = str(date.day).zfill(2)
    month = str(date.month).zfill(2)
    year = date.year

    return f"{hours}:{minutes} {am_pm} {day}/{month}/{year}"

