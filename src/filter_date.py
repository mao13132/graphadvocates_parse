from dateutil import parser

from datetime import datetime, timedelta, timezone


class FilterDate:
    @staticmethod
    def check_data(date, filter_count):
        post_time = parser.parse(date)

        target_time = datetime.now(timezone.utc) - post_time

        if target_time > timedelta(filter_count):
            return False

        return post_time

    @staticmethod
    def get_format(date: str):

        try:
            return parser.parse(date)
        except:
            return date
