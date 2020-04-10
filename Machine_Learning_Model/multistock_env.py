import numpy as np
from itertools import product


class MultiStockEnv:
    def __init__(self, data, initial_investment):
        self.data = data
        self.number_of_dates, self.number_of_stocks = self.data.shape

        self.initial_investment = initial_investment
        self.current_date = None
        self.stock_owend = None
        self.stock_price =  None
        self.cash_in_hand = None
        self.action_permutations = np.arange(3**self.number_of_stocks)
        # actions: buy, sell, hold

        self.action_list = list(map(list,
                        product([0,1,2], repeat=self.number_of_stocks)
                        ))
        # itertools.product returns cartesian product, repeat means number of elements in product
        # 0=sell, 1=hold, 2=buy
        # -> (0,0,0), (0,0,1), (0,0,2), (0,1,0), (0,1,1), (0,1,2), (0,2,1), (0,2,2)...
        # list(map(list, ['dog', 'cat'])) --> [['d','o','g'],['c','a','t']]

        self.status_size = self.number_of_stocks * 2 + 1
        # 3 states: state1(shares_owned), [3,5,7] 3 AAPL, 5 MSI, 7 SBUX
        #           state2(stock_price), [50,20,30]
        #           state3(cash_in_hand), 100(uninvested)
        # total states = [3,5,7,50,20,30,100], 2*number_of_stocks+1

        self.reset()

    def reset(self):
        self.current_date = 0
        self.stock_owend = np.zeros(self.number_of_stocks)
        self.stock_price = self.data[self.current_date]
        self.cash_in_hand = self.initial_investment
        return self.get_status()

    def step(self, index_of_action):
        assert index_of_action in self.action_permutations
        previous_value = self.get_value()
        self.current_date += 1
        self.stock_price = self.data[self.current_date]

        self.trade(index_of_action)
        current_value = self.get_value()
        reward = current_value - previous_value
        is_done = self.current_date == self.number_of_dates-1

        value = {'current_value': current_value}
        return self.get_status(), reward, is_done, value

    def get_status(self):
        status = np.empty(self.status_size)
        status[:self.number_of_stocks] = self.stock_owend
        status[self.number_of_stocks: 2*self.number_of_stocks] = self.stock_price
        status[-1] = self.cash_in_hand
        return status

    def get_value(self):
        return self.stock_owend.dot(self.stock_price) + self.cash_in_hand
        # numpy.dot() matrix multiplication

    def trade(self, index_of_action):
        chosen_action = self.action_list[index_of_action]
        sell_index = []
        buy_index = []
        # i is index, a is element in enumerate
        for i, a in enumerate(chosen_action):
            if a==0 : # 0 == sell, 1 == hold, 2 == buy
                sell_index.append(i)
            elif a == 2:
                buy_index.append(i)

        if sell_index:
            for i in sell_index:
                self.cash_in_hand += self.stock_price[i] * self.stock_owend[i]
                self.stock_owend[i] = 0
        if buy_index:
            can_buy = True
            for i in buy_index:
                if self.cash_in_hand > self.stock_price[i]:
                    self.stock_owend[i] += 1
                    self.cash_in_hand -= self.stock_price[i]
                else:
                    can_buy = False
