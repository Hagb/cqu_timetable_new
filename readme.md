# ICS 课程表文件生成脚本
适用于最新选课站点生成的 `xlsx` 格式的课表转换为日历软件能认到的 `ICS` 格式文件.
## 使用说明
使用 pip 安装依赖：
```bash
pip install .
```

### 直接运行 (demo)
准备从新选课网站下载的 `课表.xlsx` 或者 json 文件，放置于任意目录。</br>
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
pip install .[tk]
```
之后可运行
```bash
cqu_timetable_new-tk
```
启动 tkinter 前端。

###  Qt5 前端

使用 pip 安装依赖：
```bash
pip install .[pyqt]
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

demo 可见于 [main.py](main.py) 中的 `main` 函数

## FAQ
Q: 为什么不带有登录功能？</br>
A： 因为我懒。如果你能做出带有登录功能的脚本请随意 pr 。我只信得过可以下载的自动生成的课表。
（主要还是依赖项少一些）
## 姊妹项目
[cm-http-api](https://github.com/weearc/cm-http-api) （开发中）
## LICENSES
AGPLv3
