from rest_framework.serializers import DurationField as LameDurationField
from rest_framework.exceptions import ValidationError
from datetime import timedelta
import re
import math

__all__ = ["DurationIsoField"]


def to_iso8601(value: timedelta, force_int=True) -> str:
    seconds = value.total_seconds()

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks = 0
    if days > 99:
        weeks = math.ceil((days-99)/7)
        days -= weeks*7

    # if weeks > 99:
    #    raise ValueError("timedelta too long (must be under 100 weeks, 99 days, 23h, 59min, 59.999999s)")

    weeks, days, hours, minutes = map(int, (weeks, days, hours, minutes))
    seconds = round(seconds, 6)

    period = "P"
    if weeks:
        period += "{:02}W".format(weeks)
    if days or weeks:
        period += "{:02}D".format(days)

    if hours or minutes or seconds or not (weeks or days):
        period += "T"

        bigger_exists = hours
        if bigger_exists:
            period += "{:02}H".format(hours)

        # minutes
        bigger_exists = bigger_exists or minutes
        if bigger_exists:
            period += "{:02}M".format(minutes)

        # seconds
        if isinstance(seconds, int) or force_int:
            period += "{:02}S".format(int(seconds))
        else:
            # 9 chars long w/leading 0, 6 digits after decimal
            period += "%09.6fS" % seconds

    return period


def from_iso8601(value: str, strict: bool = True) -> timedelta:
    pattern = r"^P(?:(?P<weeks>\d+)W)?(?:(?P<days>\d+)D)?" \
              r"(?:T(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+(\.\d+)?)S)?)?$"

    match = re.match(pattern, value)
    if not match:
        raise ValueError("Invalid duration value: {}".format(value))

    weeks = int(match.group("weeks") or 0)
    days = int(match.group("days") or 0)
    hours = int(match.group("hours") or 0)
    minutes = int(match.group("minutes") or 0)
    seconds = float(match.group("seconds") or 0)

    if strict:
        if seconds > 59:
            raise ValueError("{} is not a valid amount of seconds. must be at least 0 and no more than 59".format(seconds))
        if minutes > 59:
            raise ValueError("{} is not a valid amount of minutes. must be at least 0 and no more than 59".format(minutes))
        if hours > 23:
            raise ValueError("{} is not a valid amount of hours. must be at least 0 and no more than 23".format(hours))
    return timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days, weeks=weeks)


class DurationIsoField(LameDurationField):

    def to_internal_value(self, value):
        if isinstance(value, timedelta):
            return timedelta

        try:
            parsed = from_iso8601(str(value), strict=False)
            if parsed is not None:
                return parsed
        except ValueError as e:
            raise ValidationError(e.args[0])

    def to_representation(self, value):
        return to_iso8601(value)
