import tushare as ts
import numpy as np
import xlwt
import time as t
import os


class Func:
    def __init__(self):
        self.info = ""

    def current_time_between(self, start_time, end_time):
        """
        判断当前时间是否在一个时间区间内

        :param start_time: 起始时间, "%H:%M"
        :type start_time: str
        :param end_time: 结束时间, "%H:%M"
        :type end_time: str
        :return: True / False
        :rtype: boolean
        """
        self.info = "Successfully!"
        return start_time < t.strftime("%H:%M") < end_time

    def format_print(self, list_):
        """
        输出三大盘的涨跌, 带颜色

        :param list_: 大盘信息
        :type list_: list

        :return: 带颜色的大盘信息
        :rtype: str
        """
        if list_[-1] > 0:
            print(list_[1], ": \033[31m", list_[-1], "\033[0m")
        elif list_[-1] < 0:
            print(list_[1], ": \033[32m", list_[-1], "\033[0m")
        else:
            print(list_[1], ": ", list_[-1])
        self.info = "Successfully print!"

    def timedelta_run(self, second, path_output, start):
        """
        每隔一段时间执行一次, 获取大盘信息

        :param second: 时间间隔, 单位秒
        :type second: int
        :param path_output: 输出文件路径
        :type path_output: str
        :param start: 起始索引
        :type start: int

        """
        index = start
        date = t.strftime("%Y-%m-%d")
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet(date)
        worksheet.write(0, 1, "上证指数")
        worksheet.write(0, 2, "深证成指")
        worksheet.write(0, 3, "创业板R")
        while self.current_time_between("09:30", "11:31") or self.current_time_between("13:00", "15:01"):
            index += 1
            df = ts.get_index()
            time = t.strftime("%H:%M:%S")
            nf = np.array(df)
            worksheet.write(index, 0, time)
            worksheet.write(index, 1, nf[0][2])
            worksheet.write(index, 2, nf[12][2])
            worksheet.write(index, 3, nf[-1][2])
            self.format_print(nf[0][:3])
            self.format_print(nf[12][:3])
            self.format_print(nf[-1][:3])
            print()
            t.sleep(second)
        if t.strftime("%H") < "12":
            ll = path_output.split(".")
            path_output = ll[0] + "-Morning." + ll[1]
        else:
            ll = path_output.split(".")
            path_output = ll[0] + "-Afternoon." + ll[1]
        workbook.save(path_output)

    def make_dir(self, dirs):
        """
        如果目录不存在, 新建目录

        :param dirs: 目录
        :type dirs: str
        """
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        self.info = "Successfully make directory!"

    def run(self, dirs, second, path_output, start):
        """
        主程序

        :param dirs: 输出文件目录
        :type dirs: str
        :param second: 时间间隔, 单位秒
        :type second: int
        :param path_output: 输出文件路径
        :type path_output: str
        :param start: 起始索引
        :type start: int
        """
        while True:
            if self.current_time_between("09:30", "11:31") or self.current_time_between("13:00", "15:01"):
                self.make_dir(dirs)
                self.timedelta_run(second=second, path_output=path_output, start=start)
            else:
                print(t.strftime("%H:%M"), ": 不在交易时间内！！！")
                return


if __name__ == '__main__':
    # 目标目录
    directory = "Excel/" + t.strftime("%Y-%m-%d")

    # 目标文件
    path = "Excel/" + t.strftime("%Y-%m-%d") + "/" + t.strftime("%Y-%m-%d") + ".xlsx"

    func = Func()

    # 入口程序
    func.run(dirs=directory, second=10, path_output=path, start=0)
