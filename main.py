import pandas as pd
import numpy as np
from icalendar import Calendar, Event, Alarm, Timezone, vDDDTypes
import re, uuid, datetime, pytz, os

VTIMEZONE = Timezone.from_ical("""BEGIN:VTIMEZONE
TZID:Asia/Shanghai
X-LIC-LOCATION:Asia/Shanghai
BEGIN:STANDARD
TZNAME:CST
TZOFFSETFROM:+0800
TZOFFSETTO:+0800
DTSTART:19700101T000000
END:STANDARD
END:VTIMEZONE""")
TIMEZONE = VTIMEZONE.to_tz()
base_dir = '/home/ddqi/kb.xlsx'
start_date = '20210301'
year = '2021'
month = '03'
day = '01'
dt = datetime.datetime(int(year),int(month),int(day),tzinfo=TIMEZONE)
time_dict = {
    1: [(8, 30), (9, 15)],
    2: [(9, 25), (10, 10)],
    3: [(10, 30), (11, 15)],
    4: [(11, 25), (12, 10)],
    5: [(13, 30), (14, 15)],
    6: [(14, 25), (15, 10)],
    7: [(15, 20), (16, 0o5)],
    8: [(16, 25), (17, 10)],
    9: [(17, 20), (18, 0o5)],
    10: [(19, 00), (19, 45)],
    11: [(19, 55), (20, 40)],
    12: [(20, 50), (21, 35)],
    13: [(21, 55), (22, 40)],
}
week_dic = {
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "日": 7,
    "全": 0,
}
tmp = []


def read_data(base_dir):
    df = np.array(pd.read_excel(base_dir, sheet_name=0))
    data = np.delete(df, 0, axis=0)
    return data


def get_schedule(data):  # 返回值说明： 开始周次，结束周次，星期几，是否整周，开始节数，结束节数
    if if_separate_time(data) is not True:
        if "星期" not in data[2]:
            all_date = list(data[2])
            del all_date[-1]
            if "-" in all_date:  # 生产实习或者实验什么的课设啥的没具体排课的
                date_during = "".join(all_date).split("-")
                return date_during[0], date_during[1], "全", True, "1", "12"
            else:  # 万一就一周呢...
                date_during = "".join(all_date)
                return date_during, date_during, "全", True, "1", "12"
        else:  # 其他具体排课了的
            date = re.split("周星期", data[2])
            week_day = date[1][0]
            if "-" in date[0]:
                start_week = date[0].split("-")[0]
                end_week = date[0].split("-")[1]
                schedule = date[1][1:-1]
                start_class = schedule.split("-")[0]
                end_class = schedule.split("-")[1]
                return start_week, end_week, week_day, False, start_class, end_class
            else:
                start_week = date[0]
                end_week = start_week
                schedule = date[1][1:-1]
                start_class = schedule.split("-")[0]
                end_class = schedule.split("-")[1]
                return start_week, end_week, week_day, False, start_class, end_class
    else:# 当带有分割的周次时候不返回任何值
        if "星期" not in data[2]:
            all_date = list(data[2])
            del all_date[-1]
            week_slice = "".join(all_date).split(",")
            for items in week_slice:
                tmp.append([data[0], data[1], items + "周", data[3], data[4]])
        else:
            date = re.split("周星期", data[2])
            all_week = date[0].split(",")
            for items in all_week:
                tmp.append([data[0], data[1], items + "周星期" + date[1], data[3], data[4]])

def add_datetime(component, name, time):
    """一个跳过带时区的时间中 VALUE 属性的 workaround

    某些日历软件无法正常解析同时带 TZID 和 VALUE 属性的时间。
    详见 https://github.com/collective/icalendar/issues/75 。
    """
    vdatetime = vDDDTypes(time)
    if 'VALUE' in vdatetime.params and 'TZID' in vdatetime.params:
        vdatetime.params.pop('VALUE')
    component.add(name, vdatetime)

def mkcal(data, cal):
    start_week, end_week, week_day, all_week, start_class, end_class = get_schedule(data)
    event = Event()
    event.add('SUMMARY', data[0])
    if data[4] is not None:
        event.add('LOCATION', data[3])
    event.add('DESCRIPTION', "教师:" + data[4] + "\n教学班号:" + data[1])

    if all_week is False:
        count = int(end_week) - int(start_week) + 1
        event.add("RRULE", {"freq": "weekly", "count": count})
        class_start_date = dt + datetime.timedelta(weeks=int(start_week) - 1, days=week_dic[week_day] - 1)
        class_start_time = datetime.timedelta(hours=time_dict[int(start_class)][0][0], minutes=time_dict[int(start_class)][0][1])
        class_end_time = datetime.timedelta(hours=time_dict[int(end_class)][1][0], minutes=time_dict[int(end_class)][1][1])
    else:
        class_start_time = datetime.timedelta(hours=8,minutes=30)
        class_end_time = datetime.timedelta(hours=21,minutes=35)
        class_start_date = dt + datetime.timedelta(weeks=int(start_week) - 1)
        count = (int(end_week) - int(start_week) + 1) * 7
        event.add("RRULE", {"freq": "daily", "count": count})

    dtstart = class_start_date + class_start_time
    dtend = class_start_date + class_end_time
    namespace = uuid.UUID(
        bytes=int(dtstart.timestamp()).to_bytes(length=8, byteorder='big') +
        int(dtend.timestamp()).to_bytes(length=8, byteorder='big')
    )

    add_datetime(event, 'DTEND', dtend)
    add_datetime(event, 'DTSTART', dtstart)
    event.add('UID', uuid.uuid3(namespace, data[0] + "-" + data[1]))

    event.add('DTSTAMP', datetime.datetime.now())
    cal.add_component(event)


def if_separate_time(data):
    if "," in data[2]:
        return True


def main():
    data = read_data(base_dir)

    cal = Calendar()
    cal.add('prodid', '-//CQU//CQU Calendar//')
    cal.add('version', '2.0')
    cal.add_component(VTIMEZONE)
    for items in data:
        if if_separate_time(items) is not True:
            mkcal(items, cal)
        else:
            get_schedule(items)
    tmp_data = np.array(tmp)
    if tmp_data.size == 0:
        f = open('timetable.ics', 'wb')
        f.write(cal.to_ical())
        f.close()
    else:
        for alter in tmp_data:
            mkcal(alter, cal)
        f = open('timetable.ics', 'wb')
        f.write(cal.to_ical())
        f.close()


if __name__ == "__main__":
    main()
