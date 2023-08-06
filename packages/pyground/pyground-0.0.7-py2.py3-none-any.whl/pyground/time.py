from datetime import date, datetime, timedelta, timezone
from numbers import Number
import re
import time

from .json import marshall


def mktimezone() -> timezone:
    """
    Create a `datetime.timezone` based on the local (current) timezone constants in the
    `time` module.
    """
    offset = time.altzone if time.daylight else time.timezone
    name = time.tzname[time.daylight]
    return timezone(timedelta(seconds=-offset), name)


def now(tz: datetime.tzinfo = None) -> datetime:
    """
    Properly always-timezone-aware version of datetime.now() from stdlib.
    """
    dt = datetime.now(tz)
    # could alternatively default tz to mktimezone() above
    if tz is None:
        dt = dt.astimezone()
    return dt


def parse_timestamp(timestamp: Number, tz: datetime.tzinfo = timezone.utc) -> datetime:
    """
    Convert epoch timestamp to datetime.
    """
    return datetime.fromtimestamp(timestamp, tz)


@marshall.register
def marshall_datetime(dt: datetime, *, timespec: str = "auto", **options) -> str:
    """
    Convert to ISO-8601 format, using Z alias for UTC.
    """
    return re.sub(r"\+00(?::00)?$", "Z", dt.isoformat(timespec=timespec))


@marshall.register
def marshall_date(d: date, **options) -> str:
    """
    Convert to ISO-8601 format.
    """
    return d.isoformat()
