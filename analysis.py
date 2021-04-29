import xlrd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


class Func:
    def __init__(self):
        self.info = ""
        self.time = []

    def data_read(self, file_path):
        """
        读取文件

        :param file_path: 文件路径
        :type file_path: str
        :return: table
        """

        wb = xlrd.open_workbook(filename=file_path)
        table = wb.sheet_by_index(0)
        self.info = "Successfully read table!"
        return table

    def create_data(self, table, option):
        """
        生成数据

        :param table: 表
        :param option: 1: 上证指数; 2: 深证成指; 3: 创业板
        :type option: int
        :return: 时间和指数的list
        """

        res = []
        rows = table.nrows  # 行数
        for i in range(rows):
            self.time.append(table.cell(i, 0).value)
            res.append(table.cell(i, option).value)
        return self.time, res

    def get_x_y(self, file_path, option):
        """
        返回x轴、y轴数据

        :param file_path: 文件目录
        :type file_path: str
        :param option: 1: 上证指数; 2: 深证成指; 3: 创业板
        :type option: int
        :return: x轴和y轴的数据
        """

        table = self.data_read(file_path)
        time, xz = self.create_data(table, option)
        return time, xz

    def plot(self, x_data, y_data):
        """
        画图

        :param x_data: x轴数据
        :type x_data: list
        :param y_data: y轴数据
        :type y_data: list
        """

        self.info = "Successfully plot"
        fig, ax = plt.subplots()
        data_x = x_data[1:]
        data_y = y_data[1:]
        ax.plot(data_x, data_y)
        plt.show()

    def get_rise(self, file_path, option):
        """
        获取上涨的区间

        :param file_path: 文件目录
        :type file_path: str
        :param option: 1: 上证指数; 2: 深证成指; 3: 创业板
        :type option: int
        """

        x_data, y_data = self.get_x_y(file_path, option)
        self.plot(x_data, y_data)


if __name__ == '__main__':
    func = Func()
    excel_path = "Excel/2021-04-23/2021-04-23-Morning.xlsx"
    opt = 1

    func.get_rise(file_path=excel_path, option=opt)
