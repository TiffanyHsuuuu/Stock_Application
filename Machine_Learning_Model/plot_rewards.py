import  matplotlib.pyplot as plt
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mode', type=str, required=True,
                    help='either "train" or "test"')
args = parser.parse_args()
data = np.load(f'rl_trader_rewards/{args.mode}.npy')
print(f"average reward: {data.mean():.2f}, min: {data.min():.2f}, max:{data.max():.2f}")
plt.hist(data, bins=20)
plt.title(args.mode)
plt.show()
