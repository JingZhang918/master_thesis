import pandas_ta as ta
import pandas as pd
import yfinance as yf

def get_data(ticker, indicator, start, end):

    df = yf.Ticker(ticker).history(start=start, end=end)[['Open', 'High', 'Low', 'Close']]

    if indicator == 'MACD':
        df.ta.macd(close='close', fast=12, slow=26, append=True)
        df['buy_signal'] = ((df.MACD_12_26_9.shift(1) < df.MACDs_12_26_9.shift(1)) & (df.MACD_12_26_9 > df.MACDs_12_26_9)).astype(int)
        df['sell_signal'] = ((df.MACD_12_26_9.shift(1) > df.MACDs_12_26_9.shift(1)) & (df.MACD_12_26_9 < df.MACDs_12_26_9)).astype(int)


    elif indicator == "RSI":
        df.ta.rsi(close='Close', length=14, append=True, signal_indicators=True, xa=70, xb=30)
        df = df.rename(columns={'RSI_14_B_30': 'buy_signal', 'RSI_14_A_70': 'sell_signal'})

    elif indicator == "SO": #Stochastic Oscillator
        df.ta.stoch(high='high', low='low', k=14, d=3, append=True)
        df['sell_signal'] = ((df.STOCHk_14_3_3 > 80) & (df.STOCHd_14_3_3 > 80) & (df.STOCHk_14_3_3 < df.STOCHd_14_3_3)).astype(int)
        df['buy_signal'] = ((df.STOCHk_14_3_3 < 20) & (df.STOCHd_14_3_3 < 20) & (df.STOCHk_14_3_3 > df.STOCHd_14_3_3)).astype(int)

    elif indicator == "ADX":
        df.ta.adx(length=14, append=True)
        df['buy_signal'] = ((df.ADX_14 > 20) & (df.DMP_14 > df.DMN_14)).astype(int)
        df['sell_signal'] = ((df.ADX_14 > 20) & (df.DMN_14 > df.DMP_14)).astype(int)

    elif indicator == "AO":# Aroon Oscillator
        df.ta.aroon(length=25, append=True)
        df['buy_signal'] = ((df.AROONU_25.shift(1) < df.AROOND_25.shift(1)) & (df.AROONOSC_25 >= 0)).astype(int)
        df['sell_signal'] = ((df.AROONU_25.shift(1) > df.AROOND_25.shift(1)) & (df.AROONOSC_25 <= 0)).astype(int)

    else:
        raise  ValueError("invalid indicator, please try again")

    df.columns = [x.lower() for x in df.columns]
    return df