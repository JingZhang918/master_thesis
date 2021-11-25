from plotly.subplots import make_subplots
import plotly.graph_objs as go
import numpy as np
import pandas as pd


def plot_indicator(price_df, save_path, ticker, indicator, signal_df=None, show_signals=False):
    # make a 2 x 1 figure
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True)

    # add candlestick on the upper subplot
    fig.append_trace(
        go.Candlestick(
            x=price_df.index,
            open=price_df.open,
            high=price_df.high,
            low=price_df.low,
            close=price_df.close,
            increasing_line_color='#ef476f',
            decreasing_line_color='#06d6a0',
            showlegend=False
        ), row=1, col=1
    )

    if indicator == "MACD":
        # plot macd on the lower subplot
        fig.append_trace(
            go.Scatter(
                x=price_df.index,
                y=price_df.macd_12_26_9,
                line=dict(color='#118ab2', width=2),
                name='macd',
                legendgroup='2',
            ), row=2, col=1
        )

        # plot signal line on the lower subplot
        fig.append_trace(
            go.Scatter(
                x=price_df.index,
                y=price_df.macds_12_26_9,
                line=dict(color='#ffd166', width=2),
                legendgroup='2',
                name='signal'
            ), row=2, col=1
        )

        # define histogram colors
        colors = np.where(price_df.macdh_12_26_9 < 0, '#06d6a0', '#ef476f')

        # add histogram on the lower subplot
        fig.append_trace(
            go.Bar(
                x=price_df.index,
                y=price_df.macdh_12_26_9,
                name='histogram',
                marker_color=colors,
            ), row=2, col=1
        )
    elif indicator == "RSI":
        # Make RSI Plot
        fig.add_trace(go.Scatter(
            x=price_df.index,
            y=price_df['rsi_14'],
            line=dict(color='#ffd166', width=2),
            #     showlegend=False,
            name="RSI"
        ), row=2, col=1
        )

        # Add upper/lower bounds
        fig.update_yaxes(range=[-10, 110], row=2, col=1)
        fig.add_hline(y=0, col=1, row=2, line_color="#666", line_width=2)
        fig.add_hline(y=100, col=1, row=2, line_color="#666", line_width=2)

        # Add overbought/oversold
        fig.add_hline(y=30, col=1, row=2, line_color='#336699', line_width=2, line_dash='dash')
        fig.add_hline(y=70, col=1, row=2, line_color='#336699', line_width=2, line_dash='dash')
    elif indicator == "SO":
        # Fast Signal (%k)
        fig.append_trace(
            go.Scatter(
                x=price_df.index,
                y=price_df['stochk_14_3_3'],
                line=dict(color='#118ab2', width=2),
                name='%K',

            ), row=2, col=1  # <------------ lower chart
        )

        # Slow signal (%d)
        fig.append_trace(
            go.Scatter(
                x=price_df.index,
                y=price_df['stochd_14_3_3'],
                line=dict(color='#ffd166', width=2),
                name='%D'
            ), row=2, col=1  # <------------ lower chart
        )

        # Extend our y-axis a bit
        fig.update_yaxes(range=[-10, 110], row=2, col=1)

        # Add upper/lower bounds
        fig.add_hline(y=0, col=1, row=2, line_color="#666", line_width=2)
        fig.add_hline(y=100, col=1, row=2, line_color="#666", line_width=2)

        # Add overbought/oversold
        fig.add_hline(y=20, col=1, row=2, line_color='#336699', line_width=2, line_dash='dash')
        fig.add_hline(y=80, col=1, row=2, line_color='#336699', line_width=2, line_dash='dash')
    elif indicator == "ADX" :
        fig.append_trace(
            go.Scatter(
                x=price_df.index,
                y=price_df.adx_14,
                line=dict(color='#ffd166', width=2),
                name='adx',
                legendgroup='2',
            ), row=2, col=1
        )
        fig.append_trace(
            go.Scatter(
                x=price_df.index,
                y=price_df.dmp_14,
                line=dict(color='#ef476f', width=2),
                legendgroup='2',
                name='+DM'
            ), row=2, col=1
        )
        fig.append_trace(
            go.Scatter(
                x=price_df.index,
                y=price_df.dmn_14,
                line=dict(color='#06d6a0', width=2),
                legendgroup='2',
                name='-DM'
            ), row=2, col=1
        )
    elif indicator == "AO" :
        fig.append_trace(
            go.Scatter(
                x=price_df.index,
                y=price_df.aroonosc_25,
                line=dict(color='#ffd166', width=2),
                name='Aroon Oscillator',
                legendgroup='2',
            ), row=2, col=1
        )
        fig.append_trace(
            go.Scatter(
                x=price_df.index,
                y=price_df.aroonu_25,
                line=dict(color='#ef476f', width=2),
                legendgroup='2',
                name='Aroon Up'
            ), row=2, col=1
        )
        fig.append_trace(
            go.Scatter(
                x=price_df.index,
                y=price_df.aroond_25,
                line=dict(color='#06d6a0', width=2),
                legendgroup='2',
                name='Aroon Down'
            ), row=2, col=1
        )
    else:
        raise ValueError("invalid indicator, please try again")

    if show_signals:
        # plot buying signal
        buying_txt =  signal_df[(signal_df.signal == 1) & (signal_df.transaction_cost > 0)]
        buying_signal = signal_df[(signal_df.signal == 1)]

        fig.append_trace(
            go.Scatter(
                x=buying_signal.date,
                y=buying_signal.transaction_price * 0.96,
                marker=dict(
                    color='#073b4c',
                    size=10,
                    line=dict(
                        color='#118ab2',
                        width=2
                    ),
                    symbol='triangle-up'

                ),
                #         mode = "markers+text",
                mode="markers",
                name="buy",
                text=buying_txt.transaction_price,
                textposition="bottom center",
                texttemplate='€%{text:.2f}',

            ), row=1, col=1
        )

        fig.append_trace(
            go.Scatter(
                x=buying_txt.date,
                y=buying_txt.transaction_price * 0.96,
                marker=dict(
                    color='#073b4c',
                    size=10,
                    line=dict(
                        color='#118ab2',
                        width=2
                    ),
                    symbol='triangle-up'

                ),
                mode="markers+text",
                #         name = "buy",
                text=buying_txt.transaction_price,
                textposition="bottom center",
                texttemplate='€%{text:.2f}',
                showlegend=False,
            ), row=1, col=1
        )

        # plot selling signal
        sell_signal = signal_df[(signal_df.signal == -1)]
        sell_txt = signal_df[(signal_df.signal == -1) & (signal_df.transaction_cost > 0)]

        fig.append_trace(
            go.Scatter(
                x=sell_signal.date,
                y=sell_signal.transaction_price * 1.04,
                marker=dict(
                    color='#fb5607',
                    size=10,
                    line=dict(
                        color='#ffbe0b',
                        width=2
                    ),
                    symbol='triangle-down'

                ),
                #         mode = "markers+text",
                mode="markers",
                name="sell",
                text=sell_txt.transaction_price,
                textposition="top center",
                texttemplate='€%{text:.2f}',
                #         textsize = 1
            ), row=1, col=1
        )

        fig.append_trace(
            go.Scatter(
                x=sell_txt.date,
                y=sell_txt.transaction_price * 1.04,
                marker=dict(
                    color='#fb5607',
                    size=10,
                    line=dict(
                        color='#ffbe0b',
                        width=2
                    ),
                    symbol='triangle-down'

                ),
                mode="markers+text",
                name="sell",
                text=sell_txt.transaction_price,
                textposition="top center",
                texttemplate='€%{text:.2f}',
                showlegend=False,
            ), row=1, col=1
        )

    # make the figure prettier
    layout = go.Layout(
        plot_bgcolor='#ecf8f8',
        font_family='Monospace',
        font_color='#073b4c',
        font_size=10,
        xaxis=dict(
            rangeslider=dict(visible=False)
        ),
        autosize=False,
        width=1000,
        height=400,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=4
        )
    )

    # ignore Saturdays and Sundays
    fig.update_xaxes(
        rangebreaks=[
            dict(bounds=['sat', 'mon'])
        ]
    )

    # plot figure
    fig.update_layout(layout)
    # fig.show()
    # print(save_path + indicator + "_" + ticker.replace(".DE","") + ".png")
    fig.write_image(save_path + indicator + "_" + ticker.replace(".DE","") + ".png")

def get_return(prices):
    return prices[-1]/prices[0]-1

def plot_monthly_return_comp_etf(df, df_etf, save_path, indicator):
    df_sum = pd.DataFrame(df.groupby(["date"]).asset.sum())
    monthly_returns = df_sum.groupby([df_sum.index.month]).asset.apply(get_return)

    etf_monthly_return = df_etf.groupby([df_etf.index.month]).Close.apply(get_return)

    # define histogram colors
    colors_macd = np.where(monthly_returns.values > 0, '#06d6a0', '#ef476f')
    colors_etf = np.where(etf_monthly_return.values > 0, '#0a9396', '#e63946')

    # add histogram on the lower subplot
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=monthly_returns.index,
            y=monthly_returns.values * 100,
            name=indicator,
            marker_color=colors_macd,
            text=monthly_returns.values * 100,
            texttemplate='%{text:.2f}',
            textposition='outside'
        ),
    )
    fig.add_trace(
        go.Bar(
            x=etf_monthly_return.index,
            y=etf_monthly_return.values * 100,
            name='ETF',
            marker_color=colors_etf,
            text=etf_monthly_return.values * 100,
            texttemplate='%{text:.2f}',
            textposition='outside'
        ),
    )

    # make the figure prettier
    layout = go.Layout(
        title="Monthly asset return comparison with ETF (%)",
        plot_bgcolor='#ecf8f8',
        font_family='Monospace',
        font_color='#073b4c',
        font_size=10,
        xaxis=dict(
            rangeslider=dict(visible=False)
        ),
        autosize=True,
    )

    fig.update_layout(layout)
    fig.write_image(save_path + indicator + "_monthly_return.png")

def plot_yearly_return_comp_etf(df, df_etf, save_path, indicator):
    df_sum = pd.DataFrame(df.groupby(["date"]).asset.sum())
    yearly_returns = df_sum.groupby([df_sum.index.year]).asset.apply(get_return)
    etf_yearly_returns = df_etf.groupby([df_etf.index.year]).Close.apply(get_return)

    # define histogram colors
    colors_macd = np.where(yearly_returns.values > 0, '#06d6a0', '#ef476f')
    colors_etf = np.where(etf_yearly_returns.values > 0, '#0a9396', '#e63946')

    # add histogram on the lower subplot
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=yearly_returns.index,
            y=yearly_returns.values * 100,
            name=indicator,
            marker_color=colors_macd,
            text=yearly_returns.values * 100,
            texttemplate='%{text:.2f}',
            textposition='outside'

        ),
    )
    fig.add_trace(
        go.Bar(
            x=etf_yearly_returns.index,
            y=etf_yearly_returns.values * 100,
            name='ETF',
            marker_color=colors_etf,
            text=etf_yearly_returns.values * 100,
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
        xaxis=dict(
            rangeslider=dict(visible=False)
        ),
        autosize=True,
    )

    fig.update_layout(layout)
    fig.write_image(save_path + indicator + "_yearly_return.png")






