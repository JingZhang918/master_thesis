import pandas as pd
import yfinance as yf
import config
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from get_data_11_26 import  get_data
from trading import get_trading_records
from visualization import plot_monthly_heatmap, plot_yearly_diff_comparison, plot_trading_behavior


def run(train_model=True, show_comp=True, show_behav=False, file_name=None):
    
    if train_model:
        # train model and get trading results
        dax_trading_records = pd.DataFrame()
        # for ticker in config.SYMBOLS:
        for ticker in ["LIN.DE"]:
            print(ticker)
            # get all data
            df = get_data(ticker, config.START, config.END)
            # trade and
            ticker_trading_records = get_trading_records(ticker, df)
            dax_trading_records = dax_trading_records.append(ticker_trading_records)
        dax_trading_records.to_excel(config.saving_path_trading_records+file_name)
    else:
        dax_trading_records = pd.read_excel(config.saving_path_trading_records+file_name)

    if show_comp:
    #     compare drl and etf
        start = datetime.strptime(config.START, "%Y-%m-%d")
        training_period = start + relativedelta(years=config.TRAINING_YEARS)
        df_etf = yf.Ticker("EXS1.DE").history(start=training_period, end=config.END)
        plot_yearly_diff_comparison(dax_trading_records, df_etf, config.saving_path_images)
        plot_monthly_heatmap(dax_trading_records, df_etf, config.saving_path_images)

    if show_behav:
        plot_trading_behavior(dax_trading_records, "ADS.DE", "2021-05-01", "2021-11-01", config.saving_path_images)

if __name__ == "__main__":
    run(train_model=True, show_comp=True, show_behav=False, file_name = "dax_trading_records_14.xlsx")
    # run(train_model=False, show_comp=False, show_behav=True, file_name = "dax_trading_records_12.xlsx")
