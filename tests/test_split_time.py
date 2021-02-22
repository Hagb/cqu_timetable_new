from datetime import date, datetime
from icalendar import Calendar, Event
from cqu_timetable_new import mkical

data = [['课名1', '教学班号1', '22-23周', '地点1', '教师1'],
        ['课名2', '教学班号2', '22-23周', '地点2', '教师2'],
        ['课名3', '教学班号3', '1-11,1,3周星期一1-2节', '地点3', '教师3'],
        ['课名4', '教学班号4', '1-11,2,3周星期一1-2,3,4-5节', '地点4', '教师4'],
        ['课名5', '教学班号5', '1-11周星期一1-2,3,4-5节', '地点5', '教师5']]


def get_clean_ical(ical):
    clean_ical = Calendar()
    for i in ical.walk('VEVENT'):
        event = Event()
        for name in 'SUMMARY', 'DTSTART', 'DTEND', 'RRULE':
            event.add(name, i[name])
        clean_ical.add_component(event)
    return clean_ical


def test_split_time(datadir):
    ical_expect = Calendar.from_ical((datadir / 'expect.ics').read_text())
    assert get_clean_ical(mkical(data, date(2021, 3, 1))) == get_clean_ical(ical_expect)
