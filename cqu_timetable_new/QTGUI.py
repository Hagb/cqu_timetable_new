#!/usr/bin/env python3

import datetime
import sys

from PySide2.QtCore import QFile, QCoreApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QFileDialog, QMessageBox

from cqu_timetable_new import load_from_xlsx, mkical


class timetable_to_ics():
    def __init__(self):
        super(timetable_to_ics, self).__init__()

        qfile = QFile('layout/mainWindow.ui')
        qfile.open(QFile.ReadOnly)
        qfile.close()
        """
        未按下按钮却执行函数可能是因为未使用 lambda
        参考：
        https://blog.csdn.net/guge907/article/details/23291763
        """
        self.ui = QUiLoader().load(qfile)
        QMessageBox.information(
            self.ui,
            "关于此程序",
            "该程序是在 AGPLv3 下发布的自由软件，源码可在 https://github.com/weearc/cqu_timetable_new 获取，欢迎在遵守该协议的情况下自由运行、拷贝、分发、学习、修改该软件。\nCopyright (C) 2021 weearc\nThis program is free software: you can redistribute it and/or modify"
            "it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version."
            "This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details."
            "You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>."
        )
        QMessageBox.warning(
            self.ui,
            "免责声明",
            "由于教务系统导出错误、人为因素、或其他不可抗力导致的课表损坏、时间未对齐等状况我们只能深表遗憾，暂无任何解决方法。\n"
            "Use at your own risk.（请自行承担使用风险）"
        )
        self.ui.BFileSelect.clicked.connect(lambda: self.file_select())
        self.ui.Bhelp.clicked.connect(lambda: self.show_help())
        self.ui.runOnBox.rejected.connect(lambda: QCoreApplication.quit())
        self.ui.runOnBox.accepted.connect(lambda: self.gen_ical(self.ui.startDate.text(),
                                                                self.ui.fileSelectText.text(),
                                                                self.ui.fileSaveText.text()))
        self.ui.BFileSave.clicked.connect(lambda: self.get_save_path())

    def get_save_path(self):
        file_fileter = "iCalendar(*.ics)"
        fd = QFileDialog.getSaveFileName(self.ui, "请选择保存位置", "timetable.ics", filter=file_fileter)
        if fd[0][-4:].lower() != ".ics":
            save_path = fd[0] + ".ics"
        else:
            save_path = fd[0]
        self.ui.fileSaveText.setText(save_path)

    def gen_ical(self, start_date, file_path, save_path):
        if all([start_date, file_path, save_path]) is False:
            QMessageBox.warning(
                self.ui,
                "错误",
                "请勿输入空值"
            )
        else:
            data = load_from_xlsx(file_path)
            isDebug = False
            year = start_date[0:4]
            month = start_date[4:6]
            day = start_date[6:]
            dt = datetime.date(int(year), int(month), int(day))
            try:
                cal = mkical(data, dt, isDebug)
                f = open(save_path, 'wb')
                f.write(cal.to_ical())
                f.close()
                QMessageBox.information(
                    self.ui,
                    "",
                    "导出完成！\n请关闭本程序并使用手机日历打开导出的 ICS 文件。"
                )
            except Exception as e:
                QMessageBox.warning(
                    self.ui,
                    "",
                    "请检查是否文件存在问题，是否存在中文文件名称以及中文路径。"
                )

    def file_select(self):
        file_fileter = "XLSX(*.xlsx)"
        fd = QFileDialog.getOpenFileName(self.ui, "请选择课表文件", filter=file_fileter)
        self.ui.fileSelectText.setText(fd[0])

    def show_help(self):
        QMessageBox.information(
            self.ui,
            "关于",
            "请从登陆选课网站 http://my.cqu.edu.cn/enroll/ ，点击“查看课表”，再点击“Excel”下载课程表数据。点击下方的“OK”后选择下载下来的文件。\n"
            "选择文件并填写行课日期，点击 OK 开始生成课表文件。"

        )

def main():
    app = QApplication([])
    app.setStyle('Fusion')
    mainWindow = timetable_to_ics()
    mainWindow.ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
