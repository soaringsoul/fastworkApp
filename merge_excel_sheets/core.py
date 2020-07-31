from fastwork.merge import MergeExcel
from PyQt5 import QtCore
import pandas as pd
import os


class Core(QtCore.QThread):
    progress_signal = QtCore.pyqtSignal(str)

    def __init__(self, excel_filepah, keep_sheetname_lst=None):
        super(Core, self).__init__()
        self.excel_filepath = excel_filepah
        self.keep_sheetname_lst = keep_sheetname_lst

    def run(self):
        self.progress_signal.emit("开始合并!")
        merge = MergeExcel(excel_filepath=self.excel_filepath)
        if type(self.keep_sheetname_lst) in [str, list] or self.keep_sheetname_lst is None:
            df_dict = merge.read_excel(excel_filepath=self.excel_filepath,
                                       sheet_name=self.keep_sheetname_lst)
            self.progress_signal.emit("当前共有%s个工作表需要合并!" % len(df_dict))
            for sheet_name, df in df_dict.items():
                self.progress_signal.emit("工作表名称【%s】: 共%s行" % (sheet_name, df.shape[0]))
            df_merge = pd.concat(df_dict)
            raw_col=[x for x in df_merge.columns]
            df_merge.index = [x[0] for x in df_merge.index]
            df_merge.index.name = '工作表名称'
            df_merge['工作表名称'] = df_merge.index
            df_merge = pd.DataFrame(df_merge, columns=['工作表名称'] + raw_col)

        else:
            self.progress_signal.emit("当前指定的参数有误！，请检查后重新输入！")
            df_merge = None

        if df_merge is not None:
            merge.to_excel(df_merge)
            new_filename = "%s_处理完成.xlsx" % os.path.basename(self.excel_filepath)
            abs_filepath = os.path.abspath(self.excel_filepath)
            new_filepath = os.path.join(os.path.dirname(abs_filepath), new_filename)
            self.progress_signal.emit('*' * 30)
            self.progress_signal.emit('*' * 30)
            self.progress_signal.emit("【合并完成】，合并后的工作表共计%s行" % df_merge.shape[0])
            self.progress_signal.emit("请到以下目录获取合并后的excel文件：\n【%s】" % new_filepath)

        # self.progress_signal.emit("合并完成")
