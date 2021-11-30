import pandas as pd
import yfinance as yf
import config
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from get_data_11_26 import  get_data
from trading import get_trading_records
from visualization import plot_monthly_heatmap, plot_yearly_diff_comparison, plot_trading_behavior


def run():
    dax_trading_records = pd.DataFrame()

    # train model and get trading results
    for ticker in config.SYMBOLS:
    # for ticker in ["ENR.DE"]:
        print(ticker)
        # get all data
        df = get_data(ticker, config.START, config.END)
        # trade and
        ticker_trading_records = get_trading_records(ticker, df)
        dax_trading_records = dax_trading_records.append(ticker_trading_records)
    dax_trading_records.to_excel(config.saving_path_trading_records+"dax_trading_records_13.xlsx")

#     compare drl and etf
    start = datetime.strptime(config.START, "%Y-%m-%d")
    training_period = start + relativedelta(years=config.TRAINING_YEARS)
    df_etf = yf.Ticker("EXS1.DE").history(start=training_period, end=config.END)
    plot_yearly_diff_comparison(dax_trading_records, df_etf, config.saving_path_images)
    plot_monthly_heatmap(dax_trading_records, df_etf, config.saving_path_images)

#     plot_trading_behavior(dax_trading_records, "LIN.DE", "2019-11-01", "2019-12-01", config.saving_path_images)

if __name__ == "__main__":
    run()
