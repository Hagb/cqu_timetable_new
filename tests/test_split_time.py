from datetime import date
from icalendar import Calendar, vDDDTypes
from cqu_timetable_new import mkical

data = [['课名1', '教学班号1', '22-23周', '地点1', '教师1'],
        ['课名2', '教学班号2', '22-23周', '地点2', '教师2'],
        ['课名3', '教学班号3', '1-5,7,9,11-13周星期一1-2节', '地点3', '教师3'],
        ['课名4', '教学班号4', '1-5,8,10,12-14周星期一1-2,4,6-8节', '地点4', '教师4'],
        ['课名5', '教学班号5', '1-6周星期一1-2,4,6-10节', '地点5', '教师5']]


def get_clean_data(ical):
    ical2 = Calendar.from_ical(ical.to_ical())
    clean_data = {}
    for i in ical2.walk('VEVENT'):
        clean_event = {}
        for name in 'SUMMARY', 'DTSTART', 'DTEND', 'RRULE':
            clean_event[name] = i[name].dt if isinstance(
                i[name], vDDDTypes) else i[name]
        clean_data[i['UID']] = clean_event
    return clean_data


def test_split_time(datadir):
    ical_expect = Calendar.from_ical((datadir / 'expect.ics').read_text())
    assert get_clean_data(mkical(data, date(2021, 3, 1))
                          ) == get_clean_data(ical_expect)
