import config
from env import StockTradingEnv

from datetime import datetime
from dateutil.relativedelta import relativedelta

import ray
from ray import tune
from ray.rllib.agents.ppo import PPOTrainer

from ray.tune.registry import register_env
from ray.tune.suggest import ConcurrencyLimiter
from ray.tune.suggest.bayesopt import BayesOptSearch

import numpy as np
import pandas as pd

def env_creator(env_config):
    return StockTradingEnv(env_config)

def get_trading_records(ticker, df):

    end = datetime.strptime(config.END, "%Y-%m-%d")

    start = datetime.strptime(config.START, "%Y-%m-%d")
    training_period = start + relativedelta(years=7)

    ray.init(ignore_reinit_error=True)

    training_data = df[df.index < training_period]
    trading_data = df[(df.index >= training_period)]

    register_env("StockTradingEnv", env_creator)

    # rap tune.ray inside
    analysis = tune.run(
        run_or_experiment=PPOTrainer
        , stop={'timesteps_total': 1e4}
        , config={
            'env': "StockTradingEnv"
            , "env_config": { 'data': training_data }
            , "seed": 0
            #             ,'lr': tune.qloguniform(1e-1, 1, 5e-5)
            #             ,'gamma': tune.uniform(0.97, 1)
            #             ,'clip_param' : tune.uniform(0.2, 0.4)
            , 'vf_clip_param': 1e4
        }
        , search_alg=ConcurrencyLimiter(
            BayesOptSearch(random_search_steps=4, metric="episode_reward_mean", mode="max"),
            max_concurrent=2
        )
        , metric="episode_reward_mean"
        , mode="max"
        , num_samples=5
        , checkpoint_at_end=True
        , verbose=0
    )

    detailed_trading_results = pd.DataFrame(columns=["ticker","date", "signal", "cash_balance", "share_holding", "asset"
                                                    ,"transaction_price", "transaction_cost", "trading_outlay", "reward"])

    agent = PPOTrainer(config=analysis.best_config, env=StockTradingEnv)
    agent.restore(analysis.best_checkpoint)

    trade_entry = {}
    dates = trading_data.index
    done = False
    env_config = {'data': trading_data }
    env = StockTradingEnv(env_config)
    obs = env.reset()

    # first day
    trade_entry["ticker"] = ticker
    trade_entry["date"] = dates[0]
    trade_entry["cash_balance"] = trade_entry["asset"] = obs[0]
    trade_entry["share_holding"] = obs[1]
    trade_entry["transaction_price"] = np.average([obs[3], obs[4]])
    trade_entry["transaction_cost"] = trade_entry["trading_outlay"] = trade_entry["reward"] = trade_entry["signal"] = 0
    detailed_trading_results = detailed_trading_results.append(trade_entry, ignore_index=True)

    i = 1
    while not done:
        trade_entry["ticker"] = ticker
        trade_entry["date"] = dates[i]
        action = agent.compute_single_action(obs)
        trade_entry["signal"] = action - 1
        obs, reward, done, info = env.step(action)

        trade_entry["cash_balance"] = obs[0]
        trade_entry["share_holding"] = obs[1]
        trade_entry["asset"] = obs[0] + obs[1] * np.average([obs[3], obs[4]])
        trade_entry["transaction_price"] = np.average([obs[3], obs[4]])
        trade_entry["transaction_cost"] = info["transaction_cost"]
        trade_entry["trading_outlay"] = info["trading_outlay"]
        trade_entry["reward"] = reward
        i += 1
        detailed_trading_results = detailed_trading_results.append(trade_entry, ignore_index=True)

    # detailed_trading_results.to_excel(saving_path + ticker + ".xlsx")

    ray.shutdown()
    return detailed_trading_results





