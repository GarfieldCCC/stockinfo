import os
import xlrd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


class Data:
    def __init__(self):
        self.info = ""

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

    def get_last_index_not_blank(self, file_path):
        """
        获取文件最后一个不为空的行索引

        :param file_path: 文件路径
        :type file_path: str
        :return: 索引值
        :rtype: int
        """
        table = self.data_read(file_path)
        row = table.nrows
        return row - 1


class Func:
    def __init__(self):
        self.info = ""
        self.time = []

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

    def plot(self, data_x, data_y, seg, title):
        """
        画出折线图

        :param data_x: x轴数据
        :param data_y: y轴数据
        :param seg: 防止x轴过于密集的分段数
        :param title: 图片标题
        :type data_x: list
        :type data_y: list
        :type seg: int
        :type title: str
        """
        self.info = "Successfully plot!"
        fig, ax = plt.subplots()
        x_data = data_x[1:]
        y_data = data_y[1:]
        ax.plot(x_data, y_data)
        ax.hlines(y=0, xmin=0, xmax=x_data.__len__(), linewidth=1, color='r', linestyles="dashed")

        tick_spacing = x_data.__len__() / seg
        ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
        plt.title(title)
        plt.show()


def main(file_path, option):
    # 函数实例化
    data = Data()
    func = Func()

    d = {1: "上证指数", 2: "深证成指", 3: "创业板"}

    # 读取数据
    table = data.data_read(file_path=file_path)

    # x轴、y轴数据
    time, xz = func.create_data(table=table, option=option)

    # 绘制折线图
    title = file_path.split("/")[-1].split(".")[0] + "-" + d[option]
    func.plot(data_x=time, data_y=xz, seg=5, title=title)


if __name__ == '__main__':
    def make_opts(path):
        d = {}
        dir_list = os.listdir(path)
        for i in range(dir_list.__len__()):
            d[i + 1] = dir_list[i]
        return d


    def print_options(opts_dict):
        for i in opts_dict:
            print(i, ": ", opts_dict[i])


    excel_path = os.getcwd().replace("\\", "/") + "/Excel/"
    print("----------------")
    opts = make_opts("Excel/")
    print_options(opts)
    print("----------------")
    opt_d = input("请选择目录: ")
    if int(opt_d) in opts:
        print("-------------------------------")
        file_opts = make_opts(excel_path + opts[int(opt_d)])
        print_options(file_opts)
        print("-------------------------------")
        opt_f = input("请选择文件: ")
        if int(opt_f) in file_opts:
            xlsx_path = excel_path + opts[int(opt_d)] + "/" + file_opts[int(opt_f)]
            opt = input("请选择: 1: 上证指数; 2: 深证成指; 3: 创业板;  0: 全部; \n")
            if -1 < int(opt) < 4:
                if int(opt) != 0:
                    main(xlsx_path, int(opt))
                    print("Success! ")
                else:
                    main(xlsx_path, 1)
                    main(xlsx_path, 2)
                    main(xlsx_path, 3)
                    print("Success! ")
            else:
                print("只能 1 or 2 or 3 ! ")
        else:
            print("不对! ")
    else:
        print("请重新输入! ")
