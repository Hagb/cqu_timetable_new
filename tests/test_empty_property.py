from datetime import date
from cqu_timetable_new import mkical
data = [['空地点', '教学班号1', '22-23周', None, '教师'],
        ['空教师', '教学班号2', '22-23周', '地点', None],
        ['空教师空地点', '教学班号2', '22-23周', None, None]
        ]


def test_empty_property():
    mkical(data, date(2021, 3, 1))
