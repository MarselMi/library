'''Кастомный фильтр для вывода колическтва дней,
сколько книга хранится у читателя'''
from datetime import datetime as dt
from django.template.defaultfilters import register
import datetime


@register.filter(name='storage_days')
def storage_days(dt_object: dt):
    diff: datetime.timedelta = dt.now().date() - dt_object
    return diff.days
