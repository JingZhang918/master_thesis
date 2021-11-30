import pandas as pd
import config
import numpy as np


def get_revised_yearly_return(df_drl) -> pd.DataFrame:
    # to deal companies with incomplete yearly data
    df_drl = df_drl.set_index(["date"])
    temp1 = \
        df_drl.groupby(["ticker", df_drl.index.year]).apply(lambda x: pd.Series({
            "count": x.asset.count(),
            "first": x.asset[0],
            "last": x.asset[-1],
        }
        ))
    temp1["days"] = [config.yearly_trading_days[y] for y in temp1.index.get_level_values(1)]
    temp1["factor"] = temp1["days"].div(temp1["count"])
    temp1["revised_return"] = (temp1["last"].div(temp1["first"])) ** temp1["factor"]
    temp1["revised_first"] = temp1["last"].div(temp1["revised_return"])

    temp2 = temp1.groupby(level=["date"])['revised_first', 'last'].apply(np.sum)
    yearly_asset_return = temp2["last"].div(temp2["revised_first"]) - 1
    yearly_reward_return = (df_drl.groupby([df_drl.index.year]).reward.apply(np.sum)).div(temp2["revised_first"])
    
    return yearly_asset_return, yearly_reward_return





def get_revised_monthly_return(df_drl) -> pd.DataFrame:
    # to deal companies with incomplete yearly data
    df_drl = df_drl.set_index(["date"])
    temp1 = \
        df_drl.groupby(["ticker", df_drl.index.year, df_drl.index.month]).apply(lambda x: pd.Series({
            "count": x.asset.count(),
            "first": x.asset[0],
            "last": x.asset[-1],
        }
        ))
    temp1.index.names = ["ticker", "year", "month"]
    temp1["days"] = [config.monthly_trading_days[y][m] for y, m in
                     zip(temp1.index.get_level_values(1), temp1.index.get_level_values(2))]
    temp1["factor"] = temp1["days"].div(temp1["count"])
    temp1["revised_return"] = (temp1["last"].div(temp1["first"])) ** temp1["factor"]
    temp1["revised_first"] = temp1["last"].div(temp1["revised_return"])
    temp2 = temp1.groupby(level=["year", "month"])['revised_first', 'last'].apply(np.sum)
    
    monthly_asset_return = temp2["last"].div(temp2["revised_first"]) - 1
    
    monthly_reward_return = (df_drl.groupby([df_drl.index.year, df_drl.index.month]).reward.apply(np.sum)).div(temp2["revised_first"])

    return monthly_asset_return, monthly_reward_return