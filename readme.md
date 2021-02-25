# ICS 课程表文件生成脚本
适用于最新选课站点生成的 `xlsx` 或 `json` 格式的课表转换为日历软件能认到的 `ICS` 格式文件.
## 使用说明
使用 pip 安装依赖：
```bash
pip install cqu_timetable_new
```

### 直接运行 (demo)
准备从新选课网站下载的 `课表.xlsx` 或者点击 `查看课表` 时请求的 json 文件，放置于任意目录。</br>
配置文件格式如下:
```editorconfig
[config]
debug = False
base_dir = /home/ddqi/kb.xlsx
start_date = 20210301
file_name = timetable.ics
```

|配置项|类型|示例|注释|
|:-|:--|:--|:--|
|debug|boolean|True|控制是否为调试模式，可选值：True False|
|base_dir|str|/home/ddqi/kb.xlsx|指向课表文件的路径|
|start_date|str|20210301|行课日期|
|file_name|str|timetable.ics|生成的 ics 文件名（为避免编码问题不要用中文），扩展名请勿更改，文件名不可包含中文|

将配置文件 `config.txt` 放置在工作目录下，终端执行：
```bash
cqu_timetable_new
```
将生成指定文件名的 iCalendar 格式文件

### tkinter 前端

使用 pip 安装依赖：
```bash
pip install cqu_timetable_new[tk]
```
之后可运行
```bash
cqu_timetable_new-tk
```
启动 tkinter 前端。

###  Qt5 前端

使用 pip 安装依赖：
```bash
pip install cqu_timetable_new[pyqt]
```
之后可运行
```bash
cqu_timetable_new-qt
```
启动 Qt5 前端。

### 作为库来使用

使用时需要先生成课表数据，再从课表数据中生成日历

1. 生成课表数据
    - 可通过 `loadIO_from_json` 或 `loadIO_from_xlsx` 函数从文件或数据流中读取 json 或 xlsx，返回解析出的课表数据
    - 也可通过 `load_from_json` 或 `load_from_xlsx` 函数读取 `str` 或 `bytes` 格式的 json 或 xlsx 数据，返回解析出的课表数据
2. 生成日历数据

    使用 `mkical` 函数，第一个参数是上一步得到的课表数据，第二个参数是 `datetime.date` 类型的开学日期，返回 `icalendar.Calendar` 类型的日历数据，可通过其 `to_ical` 得到 ics 文件的内容。

example:
```python
from cqu_timetable_new import mkical, loadIO_from_xlsx
from datetime import date
xlsx_path = "Downloads/课表.xlsx"     # 课表 xlsx 文件路径
ical_path = "课表.ics"                # 要保存的日历文件的路径
data = loadIO_from_xlsx(xlsx_path)    # 从 xlsx 文件中中加载课表数据
ical = mkical(data, date(2021,3,1))   # 生成日历，2021.3.1（必须是周一）开学
with open(ical_path, 'wb') as file_:  # 保存 ics 文件时应用二进制模式打开
    file_.write(ical.to_ical())       # 用 to_ical 方法可导出日历数据（类型为 bytes）
```

另有 demo 可见于 [cqu\_timetable\_new/\_\_init\_\_.py](cqu_timetable_new/__init__.py) 中的 `main` 函数

## FAQ
Q: 为什么不带有登录功能？</br>
A： 因为我懒。如果你能做出带有登录功能的脚本请随意 pr 。我只信得过可以下载的自动生成的课表。
（主要还是依赖项少一些）

Q：为什么导出的日历文件中有原课表中没有的整周课程？<br/>
A：有一些课程（尤其是实验课，如果你见到有非实验课的这类课程，欢迎告诉我们）在 `已选课程` 中会显示有整周的时间段，但课表中那个时间段不会显示出来。技术性地说，是该整周时间段在 json 中的 `notArrangeTimeAndRoom`,`wholeWeekOccupy` 两个属性同时为假。我们尚不知道这些时间段的意义（如果你知道，欢迎告诉我们），如果使用 xlsx 来导入，请自行提前将 xlsx 中这些时间段对应的行删去；如果使用 json 来导入，我们默认会按照和原课表相同的处理方式处理（可以给 `loadIO_from_json` 或 `load_from_json` 传 `force_whole_week=True` 参数将这部分时间段也包含进日历里）。
## 姊妹项目
[cm-http-api](https://github.com/weearc/cm-http-api) （开发中）
## LICENSES
AGPLv3
