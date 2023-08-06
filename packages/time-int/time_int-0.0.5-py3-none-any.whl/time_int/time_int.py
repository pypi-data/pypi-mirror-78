from datetime import datetime, timedelta

"""Integer subclass to represent naive time since epoch.

TimeInt values are only good for the time between
   Jan 1, 1970 -> Apr 2, 2016
These limits are available as TimeInt.MIN and TimeInt.MAX
Within this range time is rounded to the nearest second.

The idea is to have the time small for storage while making
sort comparisons quick and easy.

Also provides a method to represent the time as a string
without extraneous parts (like including time of day when
value falls on midnight, or including seconds when value
falls on a minute etc).
"""


class TimeInt(int):
    """Integer that represents a naive time since epoch."""

    MIN = None  # Jan 1, 1970, start of epoch
    MAX = None  # Apr 2, 2106, end of epoch in 32bit

    @classmethod
    def from_datetime(cls, date_time: datetime):
        """TimeInt from a datetime object."""
        return TimeInt(date_time.timestamp())

    @classmethod
    def from_unix(cls, epoch: str) -> "TimeInt":
        """TimeInt from string like "1590177600.000000000"""
        return cls(round(float(epoch)))

    @classmethod
    def utcnow(cls) -> "TimeInt":
        """Get the TimeInt for right now in UTC time."""
        return TimeInt(round(datetime.utcnow().timestamp()))

    def get_datetime(self) -> datetime:
        return datetime.fromtimestamp(int(self))

    def get_pretty(self) -> str:
        """Get as formatted string leaving off parts that are 0 on end.

        For example, if the time lands on the hour, leave off minutes
        and seconds. If it happens to fall right on the second where
        a year changes, just give the year number etc.
        """
        dt = datetime.fromtimestamp(int(self))
        if dt.second:
            form = "%Y-%m-%d %I:%M:%S %p"
        elif dt.minute:
            form = "%Y-%m-%d %I:%M %p"
        elif dt.hour:
            form = "%Y-%m-%d %I %p"
        elif dt.day != 1:
            form = "%Y-%m-%d"
        elif dt.month != 1:
            form = "%Y-%m"
        else:
            form = "%Y"
        return dt.strftime(form)

    def trunc_year(self) -> "TimeInt":
        """Round TimeInt down to the start of year."""
        dt = datetime.fromtimestamp(int(self))
        trunc_dt = datetime(year=dt.year, month=1, day=1)
        return TimeInt(int(trunc_dt.timestamp()))

    def trunc_month(self) -> "TimeInt":
        """Round TimeInt down to the start of month."""
        dt = datetime.fromtimestamp(int(self))
        trunc_dt = datetime(year=dt.year, month=dt.month, day=1)
        return TimeInt(int(trunc_dt.timestamp()))

    def trunc_week(self) -> "TimeInt":
        """Round TimeInt down to the start of latest Sunday."""
        dt = datetime.fromtimestamp(int(self))
        # Note, for some reason weekday() from datetime has Monday as 0.
        # We tweak the results so that Sunday is 0 instead.
        week_day = (dt.weekday() + 1) % 7
        delta = timedelta(
            days=week_day, hours=dt.hour, minutes=dt.minute, seconds=dt.second
        )
        sunday_dt = dt - delta
        return TimeInt(int(sunday_dt.timestamp()))

    def trunc_day(self) -> "TimeInt":
        """Round TimeInt down to the start of day."""
        dt = datetime.fromtimestamp(int(self))
        trunc_dt = datetime(year=dt.year, month=dt.month, day=dt.day)
        return TimeInt(int(trunc_dt.timestamp()))

    def trunc_hour(self) -> "TimeInt":
        """Round TimeInt down to the start of hour."""
        dt = datetime.fromtimestamp(int(self))
        trunc_dt = datetime(year=dt.year, month=dt.month, day=dt.day, hour=dt.hour)
        return TimeInt(int(trunc_dt.timestamp()))

    def trunc_minute(self) -> "TimeInt":
        """Round TimeInt down to the start of minute."""
        dt = datetime.fromtimestamp(int(self))
        trunc_dt = datetime(
            year=dt.year, month=dt.month, day=dt.day, hour=dt.hour, minute=dt.minute
        )
        return TimeInt(int(trunc_dt.timestamp()))


TimeInt.MIN = TimeInt(0)
TimeInt.MAX = TimeInt(4_294_967_294)
