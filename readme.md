# ICS 课程表文件生成脚本
适用于最新选课站点生成的 `xlsx` 格式的课表转换为日历软件能认到的 `ICS` 格式文件.
## 使用说明
使用前下载 `课表.xlsx`并放置于任意目录。更改`base_dir`为指向课表文件的绝对路径。
并更改时间`start_date`,`year`,`month`,`day`这四个值为校历上的行课日期。
</br>
使用 pip 安装依赖：
```bash
pip install -r requirements.txt --user
```
然后直接终端执行 `python main.py` 即可.

## FAQ
Q: 为什么不带有登录功能？</br>
A： 因为我懒。如果你能做出带有登录功能的脚本请随意 pr 。我只信得过可以下载的自动生成的课表。
（主要还是依赖项少一些）

## LICENSES
AGPLv3