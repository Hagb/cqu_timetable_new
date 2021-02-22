import configparser
import datetime
import uuid
import json
from io import BytesIO
from openpyxl import load_workbook
from icalendar import Calendar, Event, Timezone, vDDDTypes


__all__ = ('mkical', 'load_from_xlsx', 'loadIO_from_xlsx',
           'load_from_json', 'loadIO_from_json')

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


def load_from_xlsx(data):
    """从 xlsx 中加载课表数据

    Args:
        data (bytes): xlsx 文件数据

    Returns:
        list[tuple]: 课表数据
    """
    return loadIO_from_xlsx(BytesIO(data))


def loadIO_from_xlsx(file):
    """从 xlsx 中加载课表数据

    Args:
        file (str or stream): xlsx 文件的文件名或数据流

    Returns:
        list[tuple]: 课表数据
    """
    ws = load_workbook(file, read_only=True, data_only=True).worksheets[0]
    return list(ws.values)[2:]


def load_from_json(data):
    """从 json 中加载课表数据

    Args:
        data (str or bytes): json 文件数据

    Returns:
        list[tuple]: 课表数据
    """
    timetable = json.loads(data)["data"]
    return [(cour["courseName"],
             cour["classNbr"],
             (cour["teachingWeekFormat"],
              cour["weekDayFormat"], cour["periodFormat"]),
             cour["roomName"],
             ','.join(i["instructorName"] for i in cour["classTimetableInstrVOList"]))
            for cour in timetable]


def loadIO_from_json(file):
    """从 json 中加载课表数据

    Args:
        file (str or stream): json 文件的文件名或数据流

    Returns:
        list[tuple]: 课表数据
    """
    return load_from_json((open(file) if isinstance(file, str) else file).read())


def split_range(string):
    result = []
    for text in string.split(','):
        range = text.split('-')
        result.append(range if len(range) == 2 else range * 2)
    return result


def get_schedule(data, isDebug=False):
    # 返回值说明： [[开始周次，结束周次], ...]，星期几，是否整周，[[开始节数，结束节数]...]
    if isDebug:
        print(data)
    if isinstance(data[2], (list, tuple)):  # 如果数据来自 json
        week_str = data[2][0]
        day_str = '星期' + data[2][1] + data[2][2] + '节' if data[2][1] else ''
    else:  # 如果数据来自 xlsx
        week_str, day_str = data[2].split('周')  # 分隔周数和星期+节数
    weeks = split_range(week_str)  # 解析周数
    if day_str:  # 非整周 day_str 为 "星期Xxx-xx节"
        return weeks, day_str[2], False, split_range(day_str[3:-1])
    else:  # 整周 day_str 为空
        return weeks, '全', True, [["1", "12"]]


def add_datetime(component, name, time):
    """一个跳过带时区的时间中 VALUE 属性的 workaround

    某些日历软件无法正常解析同时带 TZID 和 VALUE 属性的时间。
    详见 https://github.com/collective/icalendar/issues/75 。
    """
    vdatetime = vDDDTypes(time)
    if 'VALUE' in vdatetime.params and 'TZID' in vdatetime.params:
        vdatetime.params.pop('VALUE')
    component.add(name, vdatetime)


def mkevent(data, cal, dt, isDebug=False):
    if not data[0]:
        assert not (data[1] or data[2] or data[3] or data[4])
        return
    weeks, week_day, all_week, classes = get_schedule(
        data, isDebug)
    event_class = Event()
    event_class.add('SUMMARY', data[0])
    if data[3] is not None:
        event_class.add('LOCATION', data[3])
    if data[4] is not None:
        event_class.add('DESCRIPTION', "教师:" + data[4] + "\n教学班号:" + data[1])
    else:
        event_class.add('DESCRIPTION', "教学班号:" + data[1])
    for start_class, end_class in classes:
        for start_week, end_week in weeks:
            event = event_class.copy()
            if all_week is False:
                count = int(end_week) - int(start_week) + 1
                event.add("RRULE", {"freq": "weekly", "count": count})
                class_start_date = dt + \
                    datetime.timedelta(weeks=int(start_week) - 1,
                                       days=week_dic[week_day] - 1)
                class_start_time = datetime.timedelta(hours=time_dict[int(start_class)][0][0],
                                                      minutes=time_dict[int(start_class)][0][1])
                class_end_time = datetime.timedelta(hours=time_dict[int(end_class)][1][0],
                                                    minutes=time_dict[int(end_class)][1][1])
            else:
                class_start_time = datetime.timedelta(hours=8, minutes=30)
                class_end_time = datetime.timedelta(hours=21, minutes=35)
                class_start_date = dt + \
                    datetime.timedelta(weeks=int(start_week) - 1)
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


def mkical(data, start_date, isDebug=False):
    """生成日历

    Args:
        data (list[tuple]): 课表数据
        start_date (datetime.date): 开学日期，必须是星期一

    Returns:
        icalendar.Calendar: 生成的日历，可通过 `to_ical` 方法导出
    """
    if start_date.weekday() != 0:
        raise ValueError("start_date must be Monday of a week")
    cal = Calendar()
    cal.add('prodid', '-//CQU//CQU Calendar//')
    cal.add('version', '2.0')
    cal.add_component(VTIMEZONE)
    dt = datetime.datetime.combine(
        start_date, datetime.time(), tzinfo=TIMEZONE)
    for items in data:
        mkevent(items, cal, dt, isDebug)
    return cal


def main():
    config = configparser.RawConfigParser()
    config.read_file(open('config.txt'))
    isDebug = config.getboolean('config', 'debug')
    base_dir = config.get('config', 'base_dir')
    start_date = config.get('config', 'start_date')
    file_name = config.get('config', 'file_name')
    year = start_date[0:4]
    month = start_date[4:6]
    day = start_date[6:]
    dt = datetime.date(int(year), int(month), int(day))
    data = (loadIO_from_xlsx
            if base_dir[-5:].lower() == ".xlsx" else loadIO_from_json)(base_dir)
    cal = mkical(data, dt, isDebug)
    if isDebug is False:
        f = open(file_name, 'wb')
        f.write(cal.to_ical())
        f.close()


if __name__ == "__main__":
    main()
