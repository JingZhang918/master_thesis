import pandas as pd
import numpy as np


def get_trading_records(data, ticker) -> pd.DataFrame:

    trading_results = pd.DataFrame(columns=["ticker", "date","signal","cash_balance", "share_holding", "asset"
                                        , "transaction_price", "transaction_cost", "total_transaction_cost", "trading_outlay", "reward", "total_reward" ])

    initial_balance = 1000000
    initial_shares = 0

    cash_balance = initial_balance
    share_holding = initial_shares
    yesterday_flag = 0
    trading_outlay = list()
    total_reward = 0
    total_transaction_cost = 0

    for row in data.iterrows():

        reward = 0
        transaction_price = (row[1].high+row[1].low)/2
        transaction_cost = 0

        if yesterday_flag == 1: #buy

            transaction_shares = np.floor((cash_balance)/(transaction_price*_cost_rate('Frankfurt')))
            transaction_amount = transaction_price*transaction_shares
            transaction_cost = _transaction_fee('Frankfurt',yesterday_flag,transaction_amount)

            cash_balance = cash_balance-transaction_amount-transaction_cost
            share_holding = share_holding+transaction_shares

            trading_outlay.append(transaction_cost+transaction_amount)

        elif yesterday_flag == -1: #sell
            transaction_shares = share_holding
            transaction_amount = transaction_price*transaction_shares

            transaction_cost = _transaction_fee('Frankfurt',yesterday_flag,transaction_amount)

            cash_balance = cash_balance+transaction_amount-transaction_cost
            share_holding = 0
            reward = transaction_amount-transaction_cost-np.sum(trading_outlay)
            trading_outlay = list()

        asset = round(cash_balance+share_holding*transaction_price,0)
        total_reward += reward
        total_transaction_cost += transaction_cost

        trading_results = trading_results.append({"ticker": ticker, "date":row[0],"signal":yesterday_flag,"cash_balance":round(cash_balance,2)
                                                  , "share_holding":share_holding, "asset":asset
                                                  ,"transaction_price":transaction_price, "transaction_cost":transaction_cost
                                                  ,"trading_outlay": np.sum(trading_outlay),"reward":reward
                                                  ,"total_transaction_cost": total_transaction_cost, "total_reward": total_reward
                                                 }, ignore_index=True)

        # observe today's trading signal and carry out tomorrow
        if row[1].buy_signal == 1:
            yesterday_flag = 1
        elif row[1].sell_signal == 1:
            yesterday_flag = -1
        else:
            yesterday_flag = 0

    return trading_results


def _cost_rate(stock_exchange) -> float:
    if stock_exchange == 'Frankfurt':
        return 1.0006
    elif stock_exchange == 'Shanghai':
        return 1.00402
    else:
        raise ValueError("invalid stock exchange, please try agian")


def _transaction_fee(stock_exchange, signal, transaction_amount) -> float:
    '''
    @params:
        stock_exchange:    'Frankfurt' or 'Shanghai';
        signal:             1 for buy; -1 for sell
        transaction_amount: transaction price x shares
    @return:
        total transaction cost
    '''
    if stock_exchange == 'Frankfurt':

        # fees demanded by stock exchange
        transaction_fee = max(0.60, 0.000096 * transaction_amount)
        trading_fee = max(2.52, 0.000504 * transaction_amount)

        # fees demanded by Trade Republic
        if transaction_amount == 0:
            return 0
        else:
            third_party_fee = 1

        return transaction_fee + trading_fee + third_party_fee

    elif stock_exchange == 'Shanghai':
        if transaction_amount == 0:
            return 0
        commision_charge = max(transaction_amount * 0.003, 5)
        transfer_fee = transaction_amount * 0.00002
        stamp_tax = transaction_amount * 0.001

        return commision_charge + transfer_fee + stamp_tax if signal == -1 else commision_charge + transfer_fee
    else:
        return 10000000
    