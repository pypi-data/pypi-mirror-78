""" date time related functions """

import datetime as dt
import time
import random
import pytz

class DateTime:
    """Datetime contains the datetime utility functions"""
    @staticmethod
    def datetime2unix(datetime_: dt.datetime) -> int:
        """convert a datetime object into
            a unixtimestamp

        Arguments:
            datetime_(dt.datetime): datetime

        Returns:
            (int): unix timestamp

        Examples:
        ..  example_code::
            >>> from apu.time.date_time import DateTime
            >>> DateTime.unixtime2date(datetime.now())
            1234567890.123

        """

        return time.mktime(datetime_.timetuple())

    @staticmethod
    def unixtime2date(unix: float) -> dt.datetime:
        """convert a uniy timestamp to datetime object

        Arguments:
            unix(float): unix timestamp

        Returns:
            (datetime.datetime): datetime

        Examples:
        ..  example_code::
            >>> from apu.time.date_time import DateTime
            >>> DateTime.unixtime2date(1234567890.123)
            2009-02-13 23:31:30.123000
        """
        assert isinstance(unix, float), "can not convert to \
                                         datetime make sure unix \
                                         is of type int"

        return dt.datetime.utcfromtimestamp(unix)


    @staticmethod
    def add_time(datetime_: dt.datetime,
                 day: int = 0,
                 hour: int = 0,
                 minute: int = 0,
                 seconds: int = 0) -> dt.datetime:
        """ add time to a datetime object with respect to the
            timezone

            This function will keep the correct timezone

        Arguments:
            datetime_(datetime.datetime): datetime object
            day(int): days
            hour(int): hours
            seconds(int): seconds

        Returns:
            (datetime.datetime): time in the correct timezone
        """

        day = abs(day)
        hour = abs(hour)
        minute = abs(minute)
        seconds = abs(seconds)

        # calculate all in seconds
        seconds += minute * 60
        seconds += hour * 60 ** 2
        seconds += day * 24 * 60 ** 2

        # calculate timezone
        time_zone = datetime_ + dt.timezone(seconds=seconds)
        return time_zone.astimezone(pytz.utc).astimezone(time_zone.tzinfo)

    @staticmethod
    def generate(start: dt.datetime,
                 end: dt.datetime,
                 random_callback=random.Random) -> dt.datetime:
        """generate a random date.

        Arguments:
            start(datetime.datetime): start time
            end(datetime.datetime): end time
            random_callback(random.Random): random number generator

        Returns:
            (datetime.datetime): datetime

        Raises:
            ValueError: the start end oder is wrong

        Examples:
        ..  example_code::
            >>> import random
            >>> import datetime as dt
            >>> from apu.time.date_time import DateTime

            >>> rand = random.Random()
            >>> rand.seed(0)

            >>> print(DateTime.generate(start=dt.datetime(2020,1,2),
            >>>       end=dt.datetime(2020,2,3),
            >>>       random_callback=rand))
            2020-01-29 00:30:57.535096
        """
        if start > end:
            raise ValueError(f"{start} should be before {end} !!!")

        time_intervall = end - start
        random_time = time_intervall * random_callback.random()
        return start + random_time
