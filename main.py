import pandas as pd
import numpy as np
from icalendar import Calendar, Event, Alarm
import re, uuid, datetime, pytz, os

base_dir = '/home/ddqi/kb.xlsx'
start_date = '20210301'
year = '2021'
month = '03'
day = '01'
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
    else:
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


def mkcal(data, cal):
    start_day = year + "-" + month + "-" + day
    start_week, end_week, week_day, all_week, start_class, end_class = get_schedule(data)
    event = Event()
    event.add('SUMMARY', data[0])
    event.add('UID', uuid.uuid4())
    if data[4] is not None:
        event.add('LOCATION', data[3])
    event.add('DESCRIPTION', "教师:" + data[4] + "\n教学班号:" + data[1])

    if all_week is False:
        count = int(end_week) - int(start_week) + 1
        event.add("RRULE", {"freq": "weekly", "count": count})
        delta_day_start = (int(start_week) - 1) * 7 + week_dic[week_day] - 1
        dt = datetime.datetime.strptime(start_day, "%Y-%m-%d")
        class_start_date = (dt + datetime.timedelta(days=delta_day_start)).strftime("%Y%m%d")
        dt2 = datetime.datetime.strptime(class_start_date, "%Y%m%d")
        start_time_minute = time_dict[int(start_class)][0][0] * 60 + time_dict[int(start_class)][0][1]
        class_start_time = (dt2 + datetime.timedelta(minutes=start_time_minute)).strftime("%H%M%S")
        dtstart = class_start_date + "T" + class_start_time
        end_time_minute = time_dict[int(end_class)][1][0] * 60 + time_dict[int(end_class)][1][1]
        class_end_time = (dt2 + datetime.timedelta(minutes=end_time_minute)).strftime("%H%M%S")
        dtend = class_start_date + "T" + class_end_time

        event.add('DTEND;TZID=Asia/Shanghai', dtend)
        event.add('DTSTART;TZID=Asia/Shanghai', dtstart)

        timestamp = datetime.datetime.now()
        event.add('DTSTAMP;VALUE=DATE',
                  datetime.datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute,
                                    timestamp.second, tzinfo=pytz.utc))
        cal.add_component(event)

    else:
        delta_day_start = (int(start_week) - 1) * 7
        dt = datetime.datetime.strptime(start_day, "%Y-%m-%d")
        class_start_time = "083000"
        class_end_time = "213500"
        class_start_date = (dt + datetime.timedelta(days=delta_day_start)).strftime("%Y%m%d")
        count = (int(end_week) - int(start_week) + 1) * 7
        event.add("RRULE", {"freq": "daily", "count": count})

        dtstart = class_start_date + "T" + class_start_time
        dtend = class_start_date + "T" + class_end_time

        event.add('DTEND;TZID=Asia/Shanghai', dtend)
        event.add('DTSTART;TZID=Asia/Shanghai', dtstart)
        timestamp = datetime.datetime.now()
        event.add('DTSTAMP;VALUE=DATE',
                  datetime.datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute,
                                    timestamp.second, tzinfo=pytz.utc))
        cal.add_component(event)


def if_separate_time(data):
    if "," in data[2]:
        return True


def main():
    data = read_data(base_dir)
    # print(data[19])
    # get_schedule(data[31])

    cal = Calendar()
    cal.add('prodid', '-//CQU//CQU Calendar//')
    cal.add('version', '2.0')
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
