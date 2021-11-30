import numpy as np
import pandas as pd
import yfinance as yf
from data_process import get_revised_yearly_return, get_revised_monthly_return
import plotly.graph_objects as go
import config

def get_returns(prices):
    return prices[-1]/prices[0]-1

def plot_yearly_diff_comparison(df_drl, df_etf, save_path):
    #return in years
    yearly_asset_return_drl, yearly_reward_return_drl = get_revised_yearly_return(df_drl)
    yearly_return_etf = df_etf.groupby([df_etf.index.year]).Close.apply(get_returns)-config.ETF_EXPENSE

    # define histogram colors
    colors_asset_drl = np.where(yearly_asset_return_drl.values > 0, '#06d6a0', '#ef476f')
    colors_reward_drl = np.where(yearly_reward_return_drl.values > 0, '#06d6a0', '#ef476f')
    colors_etf = np.where(yearly_return_etf.values > 0, '#0a9396', '#e63946')

    # plot asset diff
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=yearly_asset_return_drl.index,
            y=yearly_asset_return_drl.values * 100,
            name="DRL",
            marker_color=colors_asset_drl,
            text=yearly_asset_return_drl.values * 100,
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
    fig.write_image(save_path+"yearly_asset_comparison.png")
    
    # plot reward diff
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=yearly_reward_return_drl.index,
            y=yearly_reward_return_drl.values * 100,
            name="DRL",
            marker_color=colors_reward_drl,
            text=yearly_reward_return_drl.values * 100,
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
        title="Yearly reward return comparison with ETF (%)",
        plot_bgcolor='#ecf8f8',
        font_family='Monospace',
        font_color='#073b4c',
        font_size=10,
        xaxis=dict( rangeslider=dict(visible=False)),
        autosize=True,
    )

    fig.update_layout(layout)
    fig.write_image(save_path+"yearly_reward_comparison.png")
    
    
    

def plot_monthly_heatmap(df_drl, df_etf, save_path):
    
    years = 6
    
    monthly_asset_return_drl, monthly_reward_return_drl = get_revised_monthly_return(df_drl)
    monthly_asset_return_drl = np.resize([np.nan]*10 + list(monthly_asset_return_drl.values) + [np.nan]*2, (years, 12))
    monthly_reward_return_drl = np.resize([np.nan]*10 + list(monthly_reward_return_drl.values) + [np.nan]*2, (years, 12))

    monthly_return_etf = df_etf.groupby([df_etf.index.year, df_etf.index.month]).Close.apply(get_returns)-config.ETF_EXPENSE
    monthly_return_etf = np.resize([np.nan] * 10 + list(monthly_return_etf.values) + [np.nan] * 2, (years, 12))

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    years = [i for i in np.arange(2016, 2021 + 1, 1)]
    colorscale = [[0, '#ef476f'], [0.5, 'white'], [1, '#06d6a0']]

    # drl asset return heatmap
    monthly_returns = monthly_asset_return_drl
    annotations = go.Annotations()
    for n, row in enumerate(monthly_returns):
        for m, val in enumerate(row):
            annotations.append(go.Annotation(text=str(round(monthly_returns[n][m] * 100, 2)), x=months[m], y=years[n],
                                             xref='x1', yref='y1', showarrow=False))
    trace = go.Heatmap(x=months, y=years, z=monthly_returns, colorscale=colorscale, showscale=True)
    fig = go.Figure(data=go.Data([trace]))
    fig['layout'].update(
        title="DRL monthly asset returns in a heatmap (%)",
        annotations=annotations,
        xaxis=go.XAxis(ticks='', side='top'),
        yaxis=go.YAxis(ticks='', ticksuffix='  '),  # ticksuffix is a workaround to add a bit of padding
        autosize=True
    )
    fig.write_image(save_path+"heatmap_DRL_asset.png")

    
    # drl reward return heatmap
    monthly_returns = monthly_reward_return_drl
    annotations = go.Annotations()
    for n, row in enumerate(monthly_returns):
        for m, val in enumerate(row):
            annotations.append(go.Annotation(text=str(round(monthly_returns[n][m] * 100, 2)), x=months[m], y=years[n],
                                             xref='x1', yref='y1', showarrow=False))
    trace = go.Heatmap(x=months, y=years, z=monthly_returns, colorscale=colorscale, showscale=True)
    fig = go.Figure(data=go.Data([trace]))
    fig['layout'].update(
        title="DRL monthly reward returns in a heatmap (%)",
        annotations=annotations,
        xaxis=go.XAxis(ticks='', side='top'),
        yaxis=go.YAxis(ticks='', ticksuffix='  '),  # ticksuffix is a workaround to add a bit of padding
        autosize=True
    )
    fig.write_image(save_path+"heatmap_DRL_reward.png")
    
    # ETF
    monthly_returns = monthly_return_etf
    annotations = go.Annotations()
    for n, row in enumerate(monthly_returns):
        for m, val in enumerate(row):
            annotations.append(go.Annotation(text=str(round(monthly_returns[n][m] * 100, 2)), x=months[m], y=years[n],
                                             xref='x1', yref='y1', showarrow=False))
    trace = go.Heatmap(x=months, y=years, z=monthly_returns, colorscale=colorscale, showscale=True)
    fig = go.Figure(data=go.Data([trace]))
    fig['layout'].update(
        title="ETF monthly returns in a heatmap (%)",
        annotations=annotations,
        xaxis=go.XAxis(ticks='', side='top'),
        yaxis=go.YAxis(ticks='', ticksuffix='  '),  # ticksuffix is a workaround to add a bit of padding
        autosize=True
    )
    fig.write_image(save_path+"heatmap_etf.png")

    # asset diff
    monthly_returns = monthly_asset_return_drl - monthly_return_etf
    annotations = go.Annotations()
    for n, row in enumerate(monthly_returns):
        for m, val in enumerate(row):
            annotations.append(go.Annotation(text=str(round(monthly_returns[n][m] * 100, 2)), x=months[m], y=years[n],
                                             xref='x1', yref='y1', showarrow=False))
    trace = go.Heatmap(x=months, y=years, z=monthly_returns, colorscale=colorscale, showscale=True)
    fig = go.Figure(data=go.Data([trace]))
    fig['layout'].update(
        title="Monthly asset return diff with ETF in a heatmap (%)",
        annotations=annotations,
        xaxis=go.XAxis(ticks='', side='top'),
        yaxis=go.YAxis(ticks='', ticksuffix='  '),  # ticksuffix is a workaround to add a bit of padding
        autosize=True
    )
    fig.write_image(save_path+"heatmap_diff_asset.png")


    # reward diff
    monthly_returns = monthly_reward_return_drl - monthly_return_etf
    annotations = go.Annotations()
    for n, row in enumerate(monthly_returns):
        for m, val in enumerate(row):
            annotations.append(go.Annotation(text=str(round(monthly_returns[n][m] * 100, 2)), x=months[m], y=years[n],
                                             xref='x1', yref='y1', showarrow=False))
    trace = go.Heatmap(x=months, y=years, z=monthly_returns, colorscale=colorscale, showscale=True)
    fig = go.Figure(data=go.Data([trace]))
    fig['layout'].update(
        title="Monthly reward return diff with ETF in a heatmap (%)",
        annotations=annotations,
        xaxis=go.XAxis(ticks='', side='top'),
        yaxis=go.YAxis(ticks='', ticksuffix='  '),  # ticksuffix is a workaround to add a bit of padding
        autosize=True
    )
    fig.write_image(save_path+"heatmap_diff_reward.png")



def plot_trading_behavior(df, ticker, start, end, save_path):
    
    candelstick = yf.Ticker(ticker).history(start=start,end=end)[["Open","High","Low","Close"]]
    candelstick.columns = [c.lower() for c in candelstick.columns]
    
    trading = df[(df["ticker"]==ticker)&(df["date"]>=start)&(df["date"]<=end)]
    
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=candelstick.index,
        open=candelstick.open,
        high=candelstick.high,
        low=candelstick.low,
        close=candelstick.close,
        increasing_line_color='#ef476f',
        decreasing_line_color='#06d6a0',
        showlegend=False
    ),
                 )
    buying_signal = trading[(trading.signal == 1)&(trading.transaction_cost>0)]
    selling_signal = trading[(trading.signal == -1)&(trading.transaction_cost>0)]

    fig.add_trace(
        go.Scatter(
            x=buying_signal.date,
            y=buying_signal.transaction_price,
            marker = dict(
                color='#073b4c',
                size=10,
                line=dict(
                    color='#118ab2',
                    width=2
                ),
                symbol='triangle-up'

            ),
            mode = "markers",
            name = "Buy",
            showlegend=True,
        ), 
    )

    fig.add_trace(
        go.Scatter(
            x=selling_signal.date,
            y=selling_signal.transaction_price,
            marker = dict(
                color='#fb5607',
                size=10,
                line=dict(
                    color='#ffbe0b',
                    width=2
                ),
                symbol='triangle-down'

            ),
            mode = "markers",
            name = "Sell",
            showlegend=True,
        ), 
    )
    layout = go.Layout(
        plot_bgcolor='#ecf8f8',
        font_family='Monospace',
        font_color='#073b4c',
        font_size=10,
        xaxis=dict(
            rangeslider=dict(visible=False)
        ),
        autosize=True
    )

    fig.update_xaxes(
        rangebreaks=[
            dict(bounds=['sat', 'mon'])
        ]
    )
    fig.update_layout(layout)
    fig.write_image(save_path+ticker+"_"+start+"_"+end+"_trading_signal.png")
    