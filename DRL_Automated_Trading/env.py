import gym
import ray
import numpy as np
from ray.rllib.agents.ppo import PPOTrainer
from ray import tune
import yfinance as yf
import pandas_ta as ta

class StockTradingEnv(gym.Env):
    def __init__(self, env_config):
        super(StockTradingEnv, self).__init__()
        
        self.initial_balance = 1e6    
        self.data = env_config['data']
        self.columns = env_config['columns']
        self.index = 0
        self.index_dates = self.data.index
        self.date_number = len(self.index_dates.unique())

        self.n_state = 1 + 1 + self.data.shape[1]
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(self.n_state,), dtype=np.float32)
        self.action_space = gym.spaces.Discrete(3) #buy, hold, sell

        self.state = self.reset()

        self.balance_record = []
        self.share_owning_record = []
        self.transaction_price_record = []
        self.transaction_cost_record = []
        self.action_record = []
        self.reward_record = []
        self.asset_record = []
        self.trade_cost = list()


    def step(self, action):
        action = action - 1

        current_balance = self.state[0]
        current_own_share = self.state[1]
        #columns: ohlcv
        self.index += 1
        high_price, low_price = self._get_market_data()[1], self._get_market_data()[2]
        transaction_price = (high_price + low_price)/2

        stock_exchange = 'Frankfurt'
        cost_rate = self._highest_cost_rate(stock_exchange)
#         cost_rate = 1.05
        transaction_cost = 0
        reward = 0

        if action == 1:
            max_share = np.floor(current_balance/(transaction_price * cost_rate ))
            transaction_shares = max_share
            transaction_amount = transaction_price*transaction_shares
            transaction_cost = self._transaction_fee(stock_exchange, action, transaction_amount)
            
            if current_balance-transaction_amount-transaction_cost >= 0:
                current_balance = current_balance-transaction_amount-transaction_cost
                current_own_share = current_own_share+transaction_shares
                self.trade_cost.append(transaction_cost+transaction_amount)
            else:
                transaction_shares = transaction_amount = transaction_cost = 0

        elif action == -1: #sell
            transaction_shares = current_own_share
       
            if transaction_shares > 0:
                transaction_amount = transaction_price*transaction_shares
                transaction_cost = self._transaction_fee(stock_exchange, action, transaction_amount)
                current_balance = current_balance+transaction_amount-transaction_cost
                current_own_share = 0
                reward = transaction_amount-transaction_cost-np.sum(self.trade_cost)
                self.trade_cost = list()
            
        self.action_record.append(action)
        self.transaction_cost_record.append(transaction_cost)
        self.transaction_price_record.append(transaction_price)
        self.balance_record.append(current_balance)
        self.share_owning_record.append(current_own_share)

        done = bool(self.index >= self.date_number - 1)
     
        next_state = np.asarray([current_balance] + [current_own_share] + self._get_market_data())
        self.state = next_state
        asset = current_balance + current_own_share * transaction_price

        self.reward_record.append(reward)
        self.asset_record.append(asset)

        info = {"trading_outlay": np.sum(self.trade_cost), "transaction_cost": transaction_cost
               ,"total_reward": np.sum(self.reward_record), "total_transaction_cost": np.sum(self.transaction_cost_record)}
                
        return self.state, reward, done, info


    def _get_market_data(self) -> list:
        '''

        :return: a list of a state's market data_storage
        '''
        dataframe = self.data.loc[self.index_dates[self.index]].sort_index()
        dataframe = dataframe[self.columns]
        return list(dataframe.values)
    
    def _transaction_fee(self, stock_exchange, signal, transaction_amount) -> float:
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

            # fees demanded by postbank
            if transaction_amount == 0:
                return 0
            elif transaction_amount <= 1200:
                third_party_fee = 9.95
            elif transaction_amount <= 2600:
                third_party_fee = 17.95
            elif transaction_amount <= 5200:
                third_party_fee = 29.95
            elif transaction_amount <= 12500:
                third_party_fee = 39.95
            elif transaction_amount <= 25000:
                third_party_fee = 54.95
            else:
                third_party_fee = 69.95

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


    def _highest_cost_rate(self, stock_exchange) -> float:
        if stock_exchange == 'Frankfurt':
            return 1.01089
        elif stock_exchange == 'Shanghai':
            return 1.00302
        else:
            return 3

    def reset(self):
        self.index = 0
        self.state = np.asarray([self.initial_balance] + [0] + self._get_market_data())
        return self.state

    def render(self, mode='detail'):

        if mode == 'detail':
            print(f"The initial balance is {self.initial_balance} and share holding is {[0]}.")

            for i in range(len(self.action_record)):
                print(f"actions about to take: {self.action_record[i]} at prices: {self.transaction_price_record[i]}"
                      f", which incurs {self.transaction_cost_record[i]} transaction costs.")
                print(
                    f"current balance: {round(self.balance_record[i],2)}, current shares holding: {self.share_owning_record[i]},"
                    f"total asset is {round(self.asset_record[i],2)}")

        elif mode == 'summary':
            print(
                f"The total asset is {round(self.asset_record[-1],2)} after {self.date_number} days of trading. The cash balance"
                f"is {round(self.balance_record[-1],2)}")
            # for i in range(len(symbols)):
            #     print(f"stock {symbols[i]} owned {self.share_owning_record[-1][i]} shares, worth of "
            #           f"{round(self.share_owning_record[-1][i] * self.transaction_price_record[-1][i],2)}")
            print(f"The total transaction cost is {round(np.sum(self.transaction_cost_record),2)}")
            annualized_return = self.asset_record[-1]/self.initial_balance-1
            print(f"The annualized return is {round(annualized_return*100,2)}%")
            temp_asset_record = self.asset_record[1:] + [0]
            returns = np.array(temp_asset_record)/np.array(self.asset_record) - 1
            standard_deviation = np.std(returns[:-1])
            sharp_ration = (annualized_return - 0.02)/standard_deviation
            print(f"standard deviation is: {round(standard_deviation*100,2)}, and the sharp ration is: {round(sharp_ration,2)}")

        elif mode == 'plot':

            time = range(self.date_number)

            fig, (ax1, ax2) = plt.subplots(2, 1)
            fig.suptitle('Performance')

            ax1.plot(time, [self.initial_balance]+self.asset_record, 'o-')
            ax1.set_ylabel('asset record')

            ax2.plot(time, [0]+self.reward_record, '.-')
            ax2.set_xlabel('time (D)')
            ax2.set_ylabel('reward record')

            plt.show()

        # elif mode == 'save_reward':
        #     f1 = open(config.RESULT_SAVE_PATH_SINGLE, "a")
        #     f1.write(f"==============================================================================\n")
        #     f1.write(f"=========================={datetime.now()}===================================\n")
        #     # f.write(f"===========================symbol: {}=====================================")
        #     f1.write(str(np.around(np.asarray(self.reward_record),2))+"\n")
        #     f1.write(str(np.around(np.asarray(self.asset_record),2))+"\n")
        #     f1.close()

        elif mode == "performance":
            print("The reward and asset records are: ")
            print(self.reward_record)
            print(self.asset_record)

        elif mode == 'record':
            return self.reward_record, self.asset_record

        elif mode == "action":
            print(f"The buy action: {self.action_record.count(1)}"
                  f", the sell action: {self.action_record.count(-1)}"
                  f", the hold action: {self.action_record.count(0)}")

        elif mode == "asset":
            return self.asset_record

        else:
            raise ValueError("Invalid Mode! Try detail/summary/plot")
            
 