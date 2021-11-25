import pandas as pd
import config
from data_process import get_data
from visualization import plot_indicator, plot_monthly_return_comp_etf, plot_yearly_return_comp_etf
from trade import get_trading_records
import yfinance as yf

def run() -> None:

    for indicator in config.TECHNICAL_INDICATORS:
        # visualize indicators from 2021-06-01 to 2021-09-30
        df = get_data(ticker="ADS.DE",indicator=indicator, start="2021-06-01", end="2021-10-01")
        plot_indicator(df, config.saving_path_indicator_visualization, "ADS.DE", indicator, show_signals=False)

        #trade on all dax 30 from 2020-11-01 to 2021-10-31
        dax_trading_records = pd.DataFrame()
        for ticker in config.SYMBOLS:
            df = get_data(ticker=ticker, indicator=indicator, start=config.pre_start_date, end=config.end_date)
            trading_data = df[df.index >= config.start_date]
            temp_trading_record = get_trading_records(trading_data, ticker)
            dax_trading_records = dax_trading_records.append(temp_trading_record)

            #visualize trading signals
            plot_indicator(trading_data, config.saving_path_indicator_signal, ticker,indicator
                           , signal_df=temp_trading_record, show_signals=True)


        df_etf = yf.Ticker("EXS1.DE").history(start=config.start_date, end=config.end_date)
        # visualize dax 30 monthly return compared with etf bassed on indicator
        plot_monthly_return_comp_etf(dax_trading_records, df_etf, config.saving_path_indicator_visualization, indicator)
        # visualize dax 30 yearly return compared with etf bassed on indicator
        plot_yearly_return_comp_etf(dax_trading_records, df_etf, config.saving_path_indicator_visualization, indicator)

        # output final results
        dax_trading_records.groupby(["ticker"]).last().to_excel(config.saving_path_trading_records+indicator+"_final.xlsx")
        dax_trading_records.to_excel(config.saving_path_trading_records+indicator+".xlsx")

if __name__ == '__main__':
    run()