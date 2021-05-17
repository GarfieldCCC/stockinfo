import dash
import time
import datetime
import tushare as ts
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from plotly.subplots import make_subplots
from dash.dependencies import Output, Input

shang_zx, shang_zy = [], []
shen_zx, shen_zy = [], []
cyb_x, cyb_y = [], []
itv = []
second = 10


def current_time_between(start_time, end_time):
    """
    判断当前时间是否在一个时间区间内

    :param start_time: 起始时间, "%H:%M"
    :type start_time: str
    :param end_time: 结束时间, "%H:%M"
    :type end_time: str
    :return: True / False
    :rtype: boolean
    """
    return start_time < time.strftime("%H:%M") < end_time


def color(dig):
    """
    判断当前时间是否在一个时间区间内

    :param dig: 起始时间, "%H:%M"
    :type dig: double
    :return: CSS字典
    :rtype: dict
    """
    return {'color': 'red'} if dig >= 0 else {'color': 'green'}


def max_increase(list_):
    """
    最大上涨数

    :param list_: 指数列表
    :type list_: list
    :return: 差值
    :rtype: double
    """
    if list_.__len__() <= 1:
        return 0
    ll = list_[0]
    bb = 0
    for i in range(1, list_.__len__()):
        bb = max(bb, list_[i] - ll)
        ll = min(ll, list_[i])
    return bb


def max_decrease(list_):
    """
    最大下跌数

    :param list_: 指数列表
    :type list_: list
    :return: 差值
    :rtype: double
    """
    if list_.__len__() <= 1:
        return 0
    ll = list_[0]
    bb = 0
    for i in range(1, list_.__len__()):
        bb = min(bb, list_[i] - ll)
        ll = max(ll, list_[i])
    return bb


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [html.H3(datetime.datetime.now().strftime("%Y-%m-%d"), id="now"),
     dcc.Graph(id='shang'),
     html.Div(id='container'),
     dcc.Interval(
         id='interval',
         interval=second * 1000,
         n_intervals=0
     )]
)


@app.callback(Output("container", "children"), Input("interval", "n_intervals"))
def data(interval):
    itv.append(interval)
    max_shang, min_shang = max(shang_zy), min(shang_zy)
    max_shen, min_shen = max(shen_zy), min(shen_zy)
    max_cyb, min_cyb = max(cyb_y), min(cyb_y)

    return html.Div([html.Table([
        html.Tr([html.Th('数据/指数'),
                 html.Th('上证指数'),
                 html.Th('深证成指'),
                 html.Th('创业板R')]),

        html.Tr([html.Td("时段最高点"),
                 html.Td(max_shang, style=color(max_shang)),
                 html.Td(max_shen, style=color(max_shen)),
                 html.Td(max_cyb, style=color(max_cyb))]),
        html.Tr([html.Td("时段最低点"),
                 html.Td(min_shang, style=color(min_shang)),
                 html.Td(min_shen, style=color(min_shen)),
                 html.Td(min_cyb, style=color(min_cyb))]),
        html.Tr([html.Td("涨/跌幅"),
                 html.Td(ts.get_index().iloc[0]['change'], style=color(ts.get_index().iloc[0]['change'])),
                 html.Td(ts.get_index().iloc[12]['change'], style=color(ts.get_index().iloc[12]['change'])),
                 html.Td(ts.get_index().iloc[-1]['change'], style=color(ts.get_index().iloc[-1]['change']))]),
        html.Tr([html.Td("首尾指数差"),
                 html.Td(shang_zy[-1] - shang_zy[0], style=color(shang_zy[-1] - shang_zy[0])),
                 html.Td(shen_zy[-1] - shen_zy[0], style=color(shen_zy[-1] - shen_zy[0])),
                 html.Td(cyb_y[-1] - cyb_y[0], style=color(cyb_y[-1] - cyb_y[0]))]),
        html.Tr([html.Td("最大涨幅"),
                 html.Td(max_increase(shang_zy)),
                 html.Td(max_increase(shen_zy)),
                 html.Td(max_increase(cyb_y))]),
        html.Tr([html.Td("最大跌幅"),
                 html.Td(max_decrease(shang_zy)),
                 html.Td(max_decrease(shen_zy)),
                 html.Td(max_decrease(cyb_y))])
    ])])


@app.callback(Output("shang", "figure"), Input("interval", "n_intervals"))
def func(interval):
    itv.append(interval)

    while current_time_between("09:30", "11:31") or current_time_between("13:00", "15:01"):
        df = ts.get_index()
        t = time.strftime("%H:%M:%S")
        shang_zx.append(t)
        shang_zy.append(df.iloc[0]['close'])
        shen_zx.append(t)
        shen_zy.append(df.iloc[12]['close'])
        cyb_x.append(t)
        cyb_y.append(df.iloc[-1]['close'])

        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("上证指数", "深证成指", "创业板R", "三大盘"))

        fig.add_trace(go.Scatter(x=shang_zx, y=shang_zy, name="上证指数"),
                      row=[1, 2], col=[1, 2])

        fig.add_trace(go.Scatter(x=[shang_zx[0], shang_zx[-1]], y=[shang_zy[0], shang_zy[-1]], name="首末指数",
                                 line=dict(
                                     color="red" if shang_zy[0] < shang_zy[-1] else "green",
                                     width=2,
                                     dash='dash'
                                 )), row=1, col=1)

        fig.add_trace(go.Scatter(x=shen_zx, y=shen_zy, name="深证成指"),
                      row=[1, 2], col=[2, 2])

        fig.add_trace(go.Scatter(x=[shen_zx[0], shen_zx[-1]], y=[shen_zy[0], shen_zy[-1]], name="首末指数",
                                 line=dict(
                                     color="red" if shen_zy[0] < shen_zy[-1] else "green",
                                     width=2,
                                     dash='dash'
                                 )), row=1, col=2)

        fig.add_trace(go.Scatter(x=cyb_x, y=cyb_y, name="创业板R"),
                      row=[2, 2], col=[1, 2])

        fig.add_trace(go.Scatter(x=[cyb_x[0], cyb_x[-1]], y=[cyb_y[0], cyb_y[-1]], name="首末指数",
                                 line=dict(
                                     color="red" if cyb_y[0] < cyb_y[-1] else "green",
                                     width=2,
                                     dash='dash'
                                 )), row=2, col=1)

        fig.update_layout(height=800, width=1200, title_text="三大盘指数可视化面板")
        if time.strftime("%H:%M") == "11:30":
            fig.write_image("Excel/" + time.strftime("%Y-%m-%d") + "/Morning.png")
        if time.strftime("%H:%M") == "15:00":
            fig.write_image("Excel/" + time.strftime("%Y-%m-%d") + "/Afternoon.png")
        return fig
    func(interval)


if __name__ == '__main__':
    app.run_server(debug=True)
