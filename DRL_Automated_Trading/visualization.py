import numpy as np
import pandas as pd
from data_process import get_revised_yearly_return, get_revised_monthly_return
import plotly.graph_objects as go

def get_returns(prices):
    return prices[-1]/prices[0]-1

def plot_yearly_diff_comparison(df_drl, df_etf, save_path):
    #how to process the missing part?
    #return in years
    yearly_return_drl = get_revised_yearly_return(df_drl)
    yearly_return_etf = df_etf.groupby([df_etf.index.year]).Close.apply(get_returns)

    # define histogram colors
    colors_macd = np.where(yearly_return_drl.values > 0, '#06d6a0', '#ef476f')
    colors_etf = np.where(yearly_return_etf.values > 0, '#0a9396', '#e63946')

    # add histogram on the lower subplot
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=yearly_return_drl.index,
            y=yearly_return_drl.values * 100,
            name="DRL",
            marker_color=colors_macd,
            text=yearly_return_drl.values * 100,
            texttemplate='%{text:.2f}',
            textposition='outside'
        ),
    )
    fig.add_trace(
        go.Bar(
            x=yearly_return_etf.index,
            y=yearly_return_etf.values * 100,
            name='ETF',
            marker_color=colors_etf,
            text=yearly_return_etf.values * 100,
            texttemplate='%{text:.2f}',
            textposition='outside'
        ),
    )

    # make the figure prettier
    layout = go.Layout(
        title="Yearly asset return comparison with ETF (%)",
        plot_bgcolor='#ecf8f8',
        font_family='Monospace',
        font_color='#073b4c',
        font_size=10,
        xaxis=dict( rangeslider=dict(visible=False)),
        autosize=True,
    )

    fig.update_layout(layout)
    fig.write_image(save_path+"yearly_comparison.png")
    # pass

def plot_monthly_heatmap(df_drl, df_etf, save_path):
    monthly_return_drl = get_revised_monthly_return(df_drl)
    monthly_return_drl = np.resize([np.nan]*10 + list(monthly_return_drl.values) + [np.nan]*2, (4, 12))
    monthly_return_etf = df_etf.groupby([df_etf.index.year, df_etf.index.month]).Close.apply(get_returns)
    monthly_return_etf = np.resize([np.nan] * 10 + list(monthly_return_etf.values) + [np.nan] * 2, (4, 12))

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    years = [i for i in np.arange(2018, 2021 + 1, 1)]
    colorscale = [[0, '#ef476f'], [0.5, 'white'], [1, '#06d6a0']]


    monthly_returns = monthly_return_drl
    annotations = go.Annotations()
    for n, row in enumerate(monthly_returns):
        for m, val in enumerate(row):
            annotations.append(go.Annotation(text=str(round(monthly_returns[n][m] * 100, 2)), x=months[m], y=years[n],
                                             xref='x1', yref='y1', showarrow=False))
    trace = go.Heatmap(x=months, y=years, z=monthly_returns, colorscale=colorscale, showscale=True)
    fig = go.Figure(data=go.Data([trace]))
    fig['layout'].update(
        title="DRL monthly returns in a heatmap (%)",
        annotations=annotations,
        xaxis=go.XAxis(ticks='', side='top'),
        yaxis=go.YAxis(ticks='', ticksuffix='  '),  # ticksuffix is a workaround to add a bit of padding
        autosize=True
    )
    fig.write_image(save_path+"heatmap_DRL.png")

    monthly_returns = monthly_return_etf
    annotations = go.Annotations()
    for n, row in enumerate(monthly_returns):
        for m, val in enumerate(row):
            annotations.append(go.Annotation(text=str(round(monthly_returns[n][m] * 100, 2)), x=months[m], y=years[n],
                                             xref='x1', yref='y1', showarrow=False))
    trace = go.Heatmap(x=months, y=years, z=monthly_returns, colorscale=colorscale, showscale=True)
    fig = go.Figure(data=go.Data([trace]))
    fig['layout'].update(
        title="DRL monthly returns in a heatmap (%)",
        annotations=annotations,
        xaxis=go.XAxis(ticks='', side='top'),
        yaxis=go.YAxis(ticks='', ticksuffix='  '),  # ticksuffix is a workaround to add a bit of padding
        autosize=True
    )
    fig.write_image(save_path+"heatmap_etf.png")

    monthly_returns = monthly_return_drl - monthly_return_etf
    annotations = go.Annotations()
    for n, row in enumerate(monthly_returns):
        for m, val in enumerate(row):
            annotations.append(go.Annotation(text=str(round(monthly_returns[n][m] * 100, 2)), x=months[m], y=years[n],
                                             xref='x1', yref='y1', showarrow=False))
    trace = go.Heatmap(x=months, y=years, z=monthly_returns, colorscale=colorscale, showscale=True)
    fig = go.Figure(data=go.Data([trace]))
    fig['layout'].update(
        title="DRL monthly returns in a heatmap (%)",
        annotations=annotations,
        xaxis=go.XAxis(ticks='', side='top'),
        yaxis=go.YAxis(ticks='', ticksuffix='  '),  # ticksuffix is a workaround to add a bit of padding
        autosize=True
    )
    fig.write_image(save_path+"heatmap_diff.png")






    pass