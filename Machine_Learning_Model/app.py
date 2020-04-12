import numpy as np
import pandas as pd
import  matplotlib.pyplot as plt
import argparse
import re
import os
import pickle
from datetime import datetime
from sklearn.preprocessing import StandardScaler

from multistock_env import MultiStockEnv
from agent import Agent
from replay_buffer import ReplayBuffer

def get_data():
    df = pd.read_csv('aapl_msi_sbux.csv')
    return df.values
    # return numpy representation of the dataframe

def get_scaler(env):
    statuses = []
    for _ in range(env.number_of_dates):
        action = np.random.choice(env.action_permutations)
        status, reward, is_done, value = env.step(action)
        statuses.append(status)
        if is_done:
            break

    # Standardize each column individaully before applying ML techniques,
    #  so that each column will have mean=0, standard deviation=1
    # [[0,0],[1,0],[0,1],[1,1]] --> [[-1,-1],[1,-1],[-1,1],[1,1]]
    scaler = StandardScaler()
    scaler.fit(statuses)
    return scaler

def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def run(agent, env, is_train, scaler, batch_size):
    status = env.reset()
    status = scaler.transform([status])
    is_done = False

    while not is_done:
        index_of_action = agent.action(status)
        next_status, reward, is_done, value = env.step(index_of_action)
        next_status = scaler.transform([next_status])
        if is_train == 'train':
            agent.update_replay_memory(status, index_of_action, reward, next_status, is_done)
            agent.replay(batch_size)
        status = next_status
    return value['current_value']


if __name__ == '__main__':

    initial_investment = 20000
    agent_count = 50
    batch_size = 32

    models_folder = 'linear_rl_trader_models'
    rewards_folder = 'linear_rl_trader_rewards'
    make_dir(models_folder)
    make_dir(rewards_folder)

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', type=str, required=True,
                        help = 'either "train" or "test"')
    args = parser.parse_args()

    data = get_data()
    number_of_dates, number_of_stocks = data.shape

    number_of_training_data = number_of_dates // 2
    training_data = data[: number_of_training_data]
    test_data = data[number_of_training_data :]

    env = MultiStockEnv(training_data, initial_investment)
    status_size = env.status_size
    action_size = len(env.action_permutations)
    agent = Agent(status_size, action_size, batch_size, number_of_stocks)
    scaler = get_scaler(env)

    portfolio_value = []

    if args.mode == 'test':
        # load previous scaler
        with open(f'{models_folder}/scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)

        env = MultiStockEnv(test_data, initial_investment)
        agent.epsilon = 0.01 # no need to run multiple episodes if y=0, it's deterministic

        # load trained weights
        agent.load(f'{models_folder}/dqn.h5')

    # run agent agent_count times
    for i in range(agent_count):
        start = datetime.now()
        value = run(agent, env, args.mode, scaler, batch_size)
        period = datetime.now() - start
        print(f"run: {i + 1}/{agent_count}, final value after running: {value:.2f}, duration:{period}")
        portfolio_value.append(value)

    # save weights when done
    if args.mode == 'train':
        agent.save(f'{models_folder}/dqn.h5')

        # save scaler
        with open(f'{models_folder}/scaler.pkl', 'wb') as f:
            pickle.dump(scaler, f)

    # save portfolio value for each run
    np.save(f'{rewards_folder}/{args.mode}.npy', portfolio_value)
