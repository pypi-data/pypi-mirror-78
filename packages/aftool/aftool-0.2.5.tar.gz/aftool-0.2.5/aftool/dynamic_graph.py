# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     aplot
   Description :
   Author :        Asdil
   date：          2020/2/27
-------------------------------------------------
   Change Activity:
                   2020/2/27:
-------------------------------------------------
"""
__author__ = 'Asdil'
import pandas as pd
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from snapshot_selenium import snapshot
from pyecharts.render import make_snapshot
import plotly
import plotly.express as px


# 统计单个列的数据
def bin_data(df, col, bins):
    """bin_data方法用于统计单列数据,
        如果是标签数据直接统计个数,
        如果是数值型数据分箱后统计

    Parameters
    ----------
    df : pandas DataFrame
    col : str
        需要统计的列名
    bins : int
        分箱间隔

    Returns
    ----------
    data : pandas.core.series.Series
    """
    if bins:
        return pd.value_counts(pd.cut(df[col], bins))
    return df[col].value_counts()


# 获取其它参数
def get_kwargs(kwargs):
    """get_kwargs方法用于其它参数,
    保存成字典,简化代码

    Parameters
    ----------
    kwargs : dict
        一些其它的画图参数

    Returns
    ----------
    'target': str or bool
        分类类标签列名
    'bins': int or bool
        分箱间隔
    'overlap': book
        不同target同一col是否重叠
    'reversal': bool
        是否旋转90度
    'title': str,
        标题
    'rotate': int
        x轴标签旋转角度
    'gap': int
        x轴同一刻度不同bar的间隔
    'theme': int
        主题索引1-14
    """
    theme = {0: 'Theme-default',
             1: ThemeType.LIGHT,
             2: ThemeType.DARK,
             3: ThemeType.CHALK,
             4: ThemeType.ESSOS,
             5: ThemeType.INFOGRAPHIC,
             6: ThemeType.MACARONS,
             7: ThemeType.PURPLE_PASSION,
             8: ThemeType.ROMA,
             9: ThemeType.ROMANTIC,
             10: ThemeType.SHINE,
             11: ThemeType.VINTAGE,
             12: ThemeType.WALDEN,
             13: ThemeType.WESTEROS,
             14: ThemeType.WONDERLAND,
             }
    params = {'target': False,
              'bins': False,
              'overlap': False,
              'reversal': False,
              'title': None,
              'rotate': 0,
              'gap': 0,
              'theme': 0,
              'save_path': False
              }
    # 先设定默认值，如果传入参数改变则改变默认值
    for key in params:
        if key in kwargs:
            params[key] = kwargs[key]
    params['theme'] = theme[params['theme']]
    return params


def get_y_axis(df, col, echart, **kwargs):
    """get_y_axis方法用于获取y轴数据

    Parameters
    ----------
    df :  pandas DataFrame
    col : str
        需要统计的列名
    echart : pyechart function
        pyechart的实例，可以使柱状图折线图
    kwargs : dict
        一些其它的画图参数

    Returns
    ----------
    data : pandas.core.series.Series
        需要data数据的index作为x轴坐标
    """
    if kwargs['target']:  # 若结合分类标签统计col列
        labels = set(df[kwargs['target']].unique())  # 获取分类标签集合
        for label in labels:
            df_tmp = df[df[kwargs['target']] == label]
            data = bin_data(df_tmp, col, kwargs['bins'])
            y_values = data.values.tolist()  # y轴的值
            if kwargs['overlap']:  # 如果需要同一col不同类标签重叠
                echart.add_yaxis(
                    f"{col} {kwargs['target']}={label}",
                    y_values,
                    stack="stack1",
                    gap=f"{kwargs['gap']}%")
            else:
                echart.add_yaxis(
                    f"{col} {kwargs['target']}={label}",
                    y_values,
                    gap=f"{kwargs['gap']}%")
    else:  # 单纯统计col列
        data = bin_data(df, col, kwargs['bins'])
        y_values = data.values.tolist()  # y轴的值
        echart.add_yaxis(f"{col}", y_values)
    return data


def get_x_axis(data, echart):
    """get_x_axis方法用于

    Parameters
    ----------
    data : pandas.core.series.Series
        需要data数据的index作为x轴坐标
    echart : pyechart function
        pyechart的实例，可以使柱状图折线图

    Returns
    ----------
    """
    # 添加x轴数据
    x_labels = pd.DataFrame(data)
    x_labels = x_labels.index.astype(str).tolist()
    echart.add_xaxis(x_labels)


def bar(df, col, **kwargs):
    """bar方法用于画柱状图

    Parameters
    ----------
    df :  pandas DataFrame
    col : str
        需要统计的列名
    kwargs : dict
        一些其它的画图参数
    Returns
    ----------
    """
    kwargs = get_kwargs(kwargs)  # 获取所有默认参数
    bar = Bar(init_opts=opts.InitOpts(theme=kwargs['theme']))
    # 添加y轴数据
    data = get_y_axis(df, col, bar, **kwargs)
    # 添加x轴数据
    get_x_axis(data, bar)

    # 全局设置
    bar.set_global_opts(
        title_opts=opts.TitleOpts(
            title=kwargs['title']), xaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(
                rotate=kwargs['rotate'])), )
    if kwargs['reversal']:  # 旋转90度
        bar.reversal_axis()
        bar.set_series_opts(label_opts=opts.LabelOpts(position="right"))
    if kwargs['save_path']:  # 保存
        bar.render(f"{kwargs['save_path']}.html")
        make_snapshot(snapshot, bar.render(), f"{kwargs['save_path']}.png")

    return bar.render_notebook()  # 直接在jupyter上显示


def scatter(df, x, y, label=None, symbol=None, mark_size=9, width=1000, height=600, title=None,
            is_show=True, save_path=None, xyrange=None):
    """scatter方法用于画动态散点图

    Parameters
    ----------
    df : pd.DataFrame
    x: str
        df中, x轴列名
    y: str
        df中, y轴列名
    label: str or None
        df中标签名称
    symbol: str or None
        df中散点形状
    mark_size: int
        散点大小
    width: int
        画布长度
    height: int
        画布高度
    title: str or None
        标题
    save_path: str or None
        保存路径必须是html
    is_show: bool
        是否显示
    xyrange: list
        固定x，y轴范围eg: [xmin, xmax, ymin, ymax]

    Returns
    ----------
    """
    fig = px.scatter(df, x=x, y=y, color=label, symbol=symbol, width=width, height=height)
    fig.update_traces(marker=dict(size=mark_size, line=dict(width=1, color='DarkSlateGrey')),
                      selector=dict(mode='markers'))
    if xyrange:
        xmin, xmax, ymin, ymax = xyrange
    else:
        xmax = df[x].max() + df[x].max() * 0.1
        xmin = df[x].min() - df[x].min() * 0.1
        ymax = df[y].max() + df[y].max() * 0.1
        ymin = df[y].min() - df[y].min() * 0.1
    fig.update_layout(template='seaborn', title=title,
                      xaxis=dict(range=[xmin, xmax]),
                      yaxis=dict(range=[ymin, ymax]))
    if save_path:
        plotly.offline.plot(fig, filename=save_path, auto_open=False)
    if is_show:
        fig.show()
