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


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [html.H3(datetime.datetime.now().strftime("%Y-%m-%d"), id="now"),
     dcc.Graph(id='shang'),
     dcc.Interval(
         id='interval',
         interval=second * 1000,
         n_intervals=0
     )]
)


@app.callback(Output("shang", "figure"), Input("interval", "n_intervals"))
def func(interval):
    itv.append(interval)

    while current_time_between("09:30", "11:31") or current_time_between("13:00", "15:01"):
        df = ts.get_index()
        t = time.strftime("%H:%M:%S")
        shang_zx.append(t)
        shang_zy.append(df.iloc[0]['change'])
        shen_zx.append(t)
        shen_zy.append(df.iloc[12]['change'])
        cyb_x.append(t)
        cyb_y.append(df.iloc[-1]['change'])

        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("上证指数", "深证成指", "创业板R", "三大盘"))

        print(shang_zx[0], shang_zx[-1], shang_zy[0], shang_zy[-1])

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
