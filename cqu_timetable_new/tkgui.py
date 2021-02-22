#!/usr/bin/env python3
import sys
try:
    import easygui
except ImportError:
    print('Please install easygui!', file=sys.stderr)
    sys.exit(1)
from cqu_timetable_new import mkical, loadIO_from_xlsx
from datetime import date

init_msg = \
    """请登陆选课网站 http://my.cqu.edu.cn/enroll/ ，点击“查看课表”，再点击“Excel”下载课程表数据。

点击下方的“OK”后选择下载下来的文件。

该程序是在 AGPLv3 下发布的自由软件，源码可在 https://github.com/weearc/cqu_timetable_new 获取，欢迎在遵守该协议的情况下自由运行、拷贝、分发、学习、修改该软件。

Copyright (C) 2021 weearc

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>."""
disclaimer = \
    """由于教务系统导出错误、人为因素或其他因素导致的课表损坏、时间未对齐等状况我们只能深表遗憾，暂无任何解决方法。
Use at your own risk.（请自行承担使用风险）"""


if not easygui.msgbox(init_msg):
    sys.exit()
if not easygui.msgbox(disclaimer, title="免责声明", ok_button="已知晓潜在的风险并自行承担"):
    sys.exit()
inputFile = easygui.fileopenbox(
    "选择下载的 excel 文件", filetypes='*.xlsx', default="*.xlsx")
if not inputFile:
    sys.exit()
dateStr = easygui.enterbox("输入开学时间（必须是周一），例：20210301",
                           title="输入开学时间", default="20210301")
try:
    ics = mkical(loadIO_from_xlsx(inputFile), date(
        int(dateStr[:4]), int(dateStr[4:6]), int(dateStr[6:])))
except Exception:
    easygui.exceptionbox("请检查输入是否有误")
    sys.exit()
outputFile = easygui.filesavebox(
    "保存的日历文件", filetypes="*.ics", default="课程表.ics")
if not outputFile:
    sys.exit()
try:
    open(outputFile, 'wb').write(ics.to_ical())
except Exception:
    easygui.exceptionbox("请检查输入是否有误")
    sys.exit()
easygui.msgbox('课程表导出成功！位于 ' + outputFile + '\n请使用日历软件打开')
