from datetime import date
from cqu_timetable_new import mkical
data = [['课名1', '教学班号1', '22-23周', '地点1', '教师1'],
        ['课名2', '教学班号2', '1-11周星期一1-2节', '地点2', '教师2']]


def test_timezone():
    ical = mkical(data, date(2021, 3, 1))
    timezone = set()
    for i in ical.walk('VENENT'):
        for name in ['DTEND', 'DTSTART']:
            assert (vtime := i.get(name))
            if vtime.dt.tzinfo and (tzname := vtime.dt.tzinfo.zone):
                timezone.add(tzname)
    vtimezones = set(str(i['TZID']) for i in ical.walk('VTIMEZONE'))
    assert vtimezones.issuperset(timezone)
