# 导入python 自带库

# 导入自定义模块

from Ui_fastwork_merge import Ui_mainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog
from core import Core

import os


class MergeExcelSheets(QtWidgets.QMainWindow, Ui_mainWindow):
    def __init__(self):
        super(MergeExcelSheets, self).__init__()
        self.setupUi(self)
        self.pushbutton_openfolder.setVisible(False)

    def setBrowerPath(self):
        pass

    def init_app(self):
        self.excel_filepath = self.lineEdit_filepath.text()
        self.textEdit.clear()

    @pyqtSlot()
    def on_open_filepath_clicked(self):
        filename = self.open_file_dialog()
        self.lineEdit_filepath.setText(filename)

    def open_file_dialog(self):
        fileName, fileType = QFileDialog.getOpenFileName(self,
                                                         "请打开一个excel文件",
                                                         r"%s" % os.getcwd(),
                                                         "文件类型(*.xlsx;*.xls);")  # 设置文件扩展名过滤

        fileName = fileName.replace('/', '\\')  # windows下需要进行文件分隔符转换
        return (fileName)

    @pyqtSlot()
    def on_pushbutton_openfolder_clicked(self):
        self.open_folder()

    @pyqtSlot()
    def on_pushbutton_start_clicked(self):
        self.init_app()
        if self.excel_filepath.endswith(".xlsx") or self.excel_filepath.endswith(".xls"):
            self.to_merge()
        else:
            self.textEdit.setText("当前输入的excel文件路径有误！请检查后重新输入！")

    def to_merge(self):
        try:
            self.textEdit.clear()
            self.merge = Core(excel_filepah=self.excel_filepath)
            self.merge.progress_signal.connect(self.progress_signal_display)
            self.merge.start()
            self.pushbutton_openfolder.setVisible(True)
        except Exception as e:
            print(e)

    def progress_signal_display(self, log_info):
        self.textEdit.append(log_info)

    def error_message(self, error_info):
        self.label_progress.setText(error_info)

    def open_folder(self):
        abs_filepath = os.path.abspath(self.excel_filepath)
        folder_path = os.path.dirname(abs_filepath)
        print(folder_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        os.system('explorer.exe /n, %s' % folder_path)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    merge = MergeExcelSheets()
    merge.show()
    sys.exit(app.exec_())
