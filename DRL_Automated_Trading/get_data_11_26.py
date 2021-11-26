
import yfinance as yf
import pandas_ta as ta

def get_data(TICKER, start, end):
    # download data

    df = yf.Ticker(TICKER).history(start=start, end=end)[['Open','High','Low','Close', 'Volume']]

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

    df = df.dropna()

    return df[df.index >= "2011-11-01"]