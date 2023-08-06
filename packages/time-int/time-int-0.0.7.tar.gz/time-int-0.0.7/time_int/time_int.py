from magic_kind import MagicKind
from datetime import datetime, timedelta

from typing import Dict, Callable

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


class TimeTruncUnit(MagicKind):
    """Values to be used as arguments to TimeInt.trunc(num=1) method"""

    YEAR: str = "year"
    MONTH: str = "month"
    WEEK: str = "week"
    DAY: str = "day"
    HOUR: str = "hour"
    MINUTE: str = "minute"


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

    def trunc(self, unit: str, num: int = 1) -> "TimeInt":
        """Combination of the trunc_* methods.

        Args:
            unit: One of the TimeTruncUnit values.
            num: like num arg in trunc_* methods, not valid for week.
        Raises:
            ValueError: if unit is not class attribute of TimeTruncUnit
            ValueError: if num is not greater than 0.
            ValueError: if unit is TimeTruncUnit.WEEK and num is anything but 1.
        Returns:
            Rounded down TimeInt value.
        """
        if unit not in TimeTruncUnit:
            expected = ", ".join(sorted([f'"{_}"' for _ in TimeTruncUnit]))
            raise ValueError(
                f'Got time trunc unit of "{unit}", but expected one of {expected}'
            )
        elif num < 1:
            raise ValueError(f"number of units must be int of 1 or more, but got {num}")
        elif num != 1 and unit == TimeTruncUnit.WEEK:
            raise ValueError(
                "When truncating to week, you can not specify a num "
                f"other than the default of 1, but got {num}"
            )
        if unit == TimeTruncUnit.WEEK:
            return self.trunc_week()
        else:
            return self._trunc_function_map[unit](self, num=num)

    def trunc_year(self, num: int = 1) -> "TimeInt":
        """Round TimeInt down to the start of year (or group of years).

        Args:
            num: round down to units of this many years since year 0. (Historically there
                 is no actual year 0, rather 1 B.C. is followed by 1 A.D. But for our
                 purposes we pretend, this means, for example, the year 2000 is grouped
                 as the start of the last century rather than the end of it).
        Returns:
            TimeInt at start of month, or group of num months.
        """
        dt = datetime.fromtimestamp(int(self))
        year = dt.year - (dt.year % num)
        trunc_dt = datetime(year=year, month=1, day=1)
        return TimeInt(int(trunc_dt.timestamp()))

    def trunc_month(self, num: int = 1) -> "TimeInt":
        """Round TimeInt down to the start of month (or group of months).
        Args:
            num: round down to units of this many months since start of year.
        Returns:
            TimeInt at start of month, or group of num months.
        """
        dt = datetime.fromtimestamp(int(self))
        # Note months of year start at 1, rather than 0, so we need shift
        # down one to make the modulo operator simulate the modulo ring of num.
        month = dt.month - ((dt.month - 1) % num)
        trunc_dt = datetime(year=dt.year, month=month, day=1)
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

    def trunc_day(self, num: int = 1) -> "TimeInt":
        """Round TimeInt down to the start of day (or group of days).

        Args:
            num: round down to units of this many days since start of month.
        Returns:
            TimeInt at start of day, or group of num days.
        """
        dt = datetime.fromtimestamp(int(self))
        # Note days of month start at 1, rather than 0, so we need shift the day
        # down one to make the modulo operator simulate the modulo ring of num.
        day = dt.day - ((dt.day - 1) % num)
        trunc_dt = datetime(year=dt.year, month=dt.month, day=day)
        return TimeInt(int(trunc_dt.timestamp()))

    def trunc_hour(self, num: int = 1) -> "TimeInt":
        """Round TimeInt down to the start of hour (or group of hours).

        Args:
            num: round down to units of this many hours since start of day.
        Returns:
            TimeInt at start of hour, or group of num hours.
        """
        dt = datetime.fromtimestamp(int(self))
        hour = dt.hour - (dt.hour % num)
        trunc_dt = datetime(year=dt.year, month=dt.month, day=dt.day, hour=hour)
        return TimeInt(int(trunc_dt.timestamp()))

    def trunc_minute(self, num: int = 1) -> "TimeInt":
        """Round TimeInt down to the start of minute (or group of minutes).

        Args:
            num: round down to units of this many hours since start of day.
        Returns:
            TimeInt at start of minute, or group of num minutes.
        """
        dt = datetime.fromtimestamp(int(self))
        minute = dt.minute - (dt.minute % num)
        trunc_dt = datetime(
            year=dt.year, month=dt.month, day=dt.day, hour=dt.hour, minute=minute
        )
        return TimeInt(int(trunc_dt.timestamp()))

    _trunc_function_map: Dict[str, Callable] = {
        TimeTruncUnit.YEAR: trunc_year,
        TimeTruncUnit.MONTH: trunc_month,
        TimeTruncUnit.WEEK: trunc_week,
        TimeTruncUnit.DAY: trunc_day,
        TimeTruncUnit.HOUR: trunc_hour,
        TimeTruncUnit.MINUTE: trunc_minute,
    }


TimeInt.MIN = TimeInt(0)
TimeInt.MAX = TimeInt(4_294_967_294)
