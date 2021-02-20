import random
from datetime import datetime, timedelta
import time
import calendar
import dateparser


class Bdatetime():
    @staticmethod
    def milisecond_timestamp_now():
        return int(time.mktime(datetime.now().timetuple())) * 1000

    @staticmethod
    def timestamp_now():
        return int(time.time())

    @staticmethod
    def timestamp_min():
        return 112067427

    @staticmethod
    def parse_date(text, default=datetime.now):
        try:
            rs = dateparser.parse(date_string=text, languages=['en'])
        except:
            return default()
        if not rs:
            return default()
        return rs

    @staticmethod
    def isocalendar():
        return str(datetime.now().isocalendar()[1])

    @staticmethod
    def get_start_week_end_week():
        now = datetime.now().date()
        start = now - timedelta(days=now.weekday())
        end = start + timedelta(days=6)

        return datetime.fromordinal(start.toordinal()), datetime.fromordinal(end.toordinal()).replace(hour=23, minute=59, second=59, microsecond=0)


if __name__ == '__main__':
    print(Bdatetime.get_start_week_end_week())
