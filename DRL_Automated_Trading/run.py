import config
from env import StockTradingEnv
from get_data_11_17 import get_data

import ray
from ray import tune
from ray.rllib.agents.ppo import PPOTrainer

from ray.tune.registry import register_env
from ray.tune.suggest import ConcurrencyLimiter
from ray.tune.suggest.bayesopt import BayesOptSearch

import numpy as np
import pandas as pd
import os

def env_creator(env_config):
    return StockTradingEnv(env_config)


def run():
    saving_path = "./results14/"
    if not os.path.isdir(saving_path):
        os.mkdir(saving_path)

    dax_trading_results = pd.DataFrame(columns=["ticker","cash_balance", "share_holding", "asset", "transaction_cost"
                                                , "total_reward" ])

    for ticker in config.SYMBOLS:

        training_data, test_data = get_data(ticker)

        ray.init(ignore_reinit_error=True)
        register_env("StockTradingEnv", env_creator)

        #rap tune.ray inside
        analysis = tune.run(
            run_or_experiment=PPOTrainer
            ,stop={'timesteps_total' : 1e4}
            ,config={
                'env': "StockTradingEnv"
                ,"env_config" : {
                    'data' : training_data
                    ,'columns' : training_data.columns
                }
                ,"seed" : 0
    #             ,'lr': tune.qloguniform(1e-1, 1, 5e-5)
    #             ,'gamma': tune.uniform(0.97, 1)
    #             ,'clip_param' : tune.uniform(0.2, 0.4)
                ,'vf_clip_param': 1e4
            }
#             ,name='test_2021_11_18_2'
            ,search_alg=ConcurrencyLimiter(
                BayesOptSearch(random_search_steps=4 ,metric = "episode_reward_mean", mode="max"),
                max_concurrent=2
            )
            ,metric = "episode_reward_mean"
            ,mode="max"
            ,num_samples=5
            ,checkpoint_at_end = True
            ,verbose = 1
        )

        detailed_trading_results = pd.DataFrame(columns=["date","signal","cash_balance", "share_holding", "asset"
                                            , "transaction_price", "transaction_cost", "trading_outlay", "reward" ])

        agent = PPOTrainer(config=analysis.best_config, env=StockTradingEnv)
        agent.restore(analysis.best_checkpoint)

        trade_entry = {}
        dates = test_data.index
        done = False
        env_config = {'data' : test_data, 'columns' : test_data.columns}
        env = StockTradingEnv(env_config)
        obs = env.reset()


        #first day
        trade_entry["date"] = dates[0]
        trade_entry["cash_balance"] = trade_entry["asset"] = obs[0]
        trade_entry["share_holding"] = obs[1]
        trade_entry["transaction_price"] = np.average([obs[3], obs[4]])
        trade_entry["transaction_cost"] = trade_entry["trading_outlay"] = trade_entry["reward"] = trade_entry["signal"] = 0
        detailed_trading_results = detailed_trading_results.append(trade_entry, ignore_index=True)

        i = 1
        while not done:
            trade_entry["date"] = dates[i]
            action = agent.compute_single_action(obs)
            trade_entry["signal"] = action-1
            obs, reward, done, info = env.step(action)

            trade_entry["cash_balance"] = obs[0]
            trade_entry["share_holding"] = obs[1]
            trade_entry["asset"] = obs[0] + obs[1]*np.average([obs[3], obs[4]])
            trade_entry["transaction_price"] = np.average([obs[3], obs[4]])
            trade_entry["transaction_cost"] = info["transaction_cost"]
            trade_entry["trading_outlay"] = info["trading_outlay"]
            trade_entry["reward"] = reward
            i+=1
            detailed_trading_results = detailed_trading_results.append(trade_entry, ignore_index=True)
        detailed_trading_results.to_excel(saving_path+ticker+".xlsx")
        ray.shutdown()

        dax_trading_results = dax_trading_results.append({"ticker": ticker, "cash_balance": obs[0], "share_holding": obs[1]
                                                         ,"asset": obs[0] + obs[1]*np.average([obs[3], obs[4]])
                                                         ,"transaction_cost": info["total_transaction_cost"]
                                                         ,"total_reward": info["total_reward"]},ignore_index=True)

    dax_trading_results.to_excel(saving_path+"DAX.xlsx")
    
    
if __name__ == "__main__":
    run()