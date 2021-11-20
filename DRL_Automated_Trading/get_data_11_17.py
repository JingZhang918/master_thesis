# training period : 2016-10-01 — 2020-09-30
# test period     : 2020-10-01 - 2021-10-01
# feature: try out only the strading signals

import yfinance as yf
import pandas_ta as ta

def get_data(TICKER):
    # download data

    df = yf.Ticker(TICKER).history(start='2016-08-01', end='2021-10-01')[['Open','High','Low','Close', 'Volume']]

    # MACD
    df.ta.macd(close='close', fast=12, slow=26, append=True)
    # MACD crossing above the signal line – Buy
    df['macd_buy'] = ((df.MACD_12_26_9.shift(1) < df.MACDs_12_26_9.shift(1)) & (df.MACD_12_26_9 > df.MACDs_12_26_9)).astype(int)
    # MACD crossing below the signal line – Sell
    df['macd_sell'] = ((df.MACD_12_26_9.shift(1) > df.MACDs_12_26_9.shift(1)) & (df.MACD_12_26_9 < df.MACDs_12_26_9)).astype(int)

    # RSI
    df.ta.rsi(close='Close', length=14, append=True, signal_indicators=True, xa=70, xb=30)
    df = df.rename(columns={'RSI_14_B_30':'rsi_buy', 'RSI_14_A_70':'rsi_sell'})

    # Stochastic Oscillator
    df.ta.stoch(high='high', low='low', k=14, d=3, append=True)
    # print(df.columns)
    df['so_sell'] = ((df.STOCHk_14_3_3>80)&(df.STOCHd_14_3_3>80)&(df.STOCHk_14_3_3<df.STOCHd_14_3_3)).astype(int)
    df['so_buy'] = ((df.STOCHk_14_3_3<20)&(df.STOCHd_14_3_3<20)&(df.STOCHk_14_3_3>df.STOCHd_14_3_3)).astype(int)

    # ADX
    df.ta.adx(length=14, append=True)
    df['adx_buy'] = ((df.ADX_14>25) & (df.DMP_14 > df.DMN_14)).astype(int)
    df['adx_sell'] = ((df.ADX_14>25) & (df.DMN_14 > df.DMP_14)).astype(int)

    # Aroon Oscillator
    df.ta.aroon(length=25, append=True)
    df['aroon_buy'] = ((df.AROONU_25.shift(1) < df.AROOND_25.shift(1)) & (df.AROONOSC_25 >= 0)).astype(int)
    df['aroon_sell'] = ((df.AROONU_25.shift(1) > df.AROOND_25.shift(1)) & (df.AROONOSC_25 <= 0)).astype(int)

    # Accumulation/Distribution Index And On-balance Volume
    df.ta.ad(append=True)
    df.ta.obv(append=True)

    df.columns = [c.lower() for c in df.columns]
    df = df.drop(columns=['macd_12_26_9','macdh_12_26_9', 'macds_12_26_9'
                          ,'rsi_14'
                          ,"stochk_14_3_3", "stochd_14_3_3"
                          ,'adx_14', 'dmp_14','dmn_14'
                          ,'aroond_25', 'aroonu_25', 'aroonosc_25'])

    integrated_data = df

    if TICKER == 'DHER.DE':
        training_start_date = '2017-08-30' #'2017-06-30'
    else:
        training_start_date = '2016-10-01'
    
#     training_start_date = '2010-10-01'
    training_end_date = '2020-10-01'
    test_start_date = '2020-10-01'
    test_end_date = '2021-10-01'

    training_data = integrated_data[(integrated_data.index >= training_start_date)*(integrated_data.index < training_end_date) ]
    test_data = integrated_data[(integrated_data.index >= test_start_date)*(integrated_data.index < test_end_date) ]

    return training_data, test_data