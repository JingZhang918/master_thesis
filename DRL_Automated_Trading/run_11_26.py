import pandas as pd
import yfinance as yf
import config
import os
from get_data_11_26 import  get_data
from trading_11_26 import get_trading_records

def run():
    dax_trading_records = pd.DataFrame()
    for ticker in ["ALV.DE","ADS.DE"]:
        print(ticker)
        # get all data
        df = get_data(ticker, config.START, config.END)
        # trade and
        ticker_trading_records = get_trading_records(ticker, df)
        dax_trading_records = dax_trading_records.append(ticker_trading_records)
    dax_trading_records.to_excel(config.saving_path_trading_records+"dax_trading_records.xlsx")
    #compare drl and etf
    # df_etf = yf.Ticker("EXS1.DE").history(start=config.start_date, end=config.end_date)
    # plot_comparison(dax_trading_records, df_etf)

if __name__ == "__main__":
    run()
