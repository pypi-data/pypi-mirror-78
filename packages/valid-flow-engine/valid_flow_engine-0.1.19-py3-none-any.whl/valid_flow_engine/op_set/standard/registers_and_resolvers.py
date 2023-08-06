from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from datetime import datetime

from ..resolver import register_resolver, ParamResolver
from ..op_set import OpSetRegistry, Op
from ..standard.comparison import ComparisonMixin
from ..standard.math import MathMixin


@OpSetRegistry.register
@register_resolver('number')
class Number(ParamResolver, ComparisonMixin, MathMixin):

    @classmethod
    def resolve(cls, data):
        num = data
        try:
            num = int(data)
        except ValueError:
            try:
                num = float(data)
            except ValueError:
                pass
        return num


@OpSetRegistry.register
@register_resolver('datetime')
@register_resolver('date')
class DateTime(ParamResolver, ComparisonMixin):
    @classmethod
    def resolve(cls, data):
        date = data
        try:
            date = parse(data)
        except Exception:
            pass
        return date

    @staticmethod
    def find_age(dob: datetime, at_date: datetime):
        try:
            birthday = dob.replace(year=at_date.year)
        except ValueError:
            birthday = dob.replace(
                year=at_date.year,
                month=dob.month + 1,
                day=1
            )
        if birthday > at_date:
            return at_date.year - dob.year - 1
        else:
            return at_date.year - dob.year

    @staticmethod
    @Op.create(key='age', ui_string='Find Age (as of today\'s date', provide_resolver=True)
    def age(dob: datetime) -> int:
        return DateTime.find_age(dob, datetime.today())

    @staticmethod
    @Op.create(key='age_at_date', ui_string='Find Age as of a provided date', provide_resolver=True)
    def age_at_date(dob: datetime, at_date: datetime) -> int:
        return DateTime.find_age(dob, at_date)

    @ staticmethod
    @ Op.create(
        key='in_age_band',
        ui_string='Determine if age is in an age band (inclusive on both ends)',
        provide_resolver=True
    )
    def in_age_band(dob: datetime, min_age: int, max_age: datetime) -> bool:
        age = DateTime.find_age(dob, datetime.today())
        return min_age < age < max_age

    @ staticmethod
    @ Op.create(
        key='year_dif',
        ui_string='Find number of years between two dates',
        provide_resolver=True
    )
    def year_dif(date: datetime, other: datetime):
        """
        This is the same as age
        """
        return (relativedelta(date, other)).years

    @ staticmethod
    @ Op.create(
        key='month_dif',
        ui_string='Find number of months between two dates',
        provide_resolver=True
    )
    def month_dif(date: datetime, other: datetime) -> int:
        delta = (relativedelta(date, other))
        return (delta.years * 12) + delta.months

    @ staticmethod
    @ Op.create(
        key='day_dif',
        ui_string='Find number of days between two dates',
        provide_resolver=True
    )
    def day_dif(date: datetime, other: datetime) -> int:
        return (date - other).days
