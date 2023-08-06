from pyground.time import parse_timestamp, marshall


def test_marshall():
    unix_epoch = parse_timestamp(0)
    assert marshall(unix_epoch) == "1970-01-01T00:00:00Z"
    assert marshall(unix_epoch, timespec="minutes") == "1970-01-01T00:00Z"
    assert marshall(unix_epoch.date()) == "1970-01-01"
