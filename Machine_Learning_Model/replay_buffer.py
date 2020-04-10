import numpy as np
import pandas as pd

class ReplayBuffer:
    def __init__(self, status_size, action_size, size):
        self.current_status = np.zeros([size, status_size], dtype=np.float32)
        self.next_status = np.zeros([size, status_size], dtype=np.float32)
        self.action = np.zeros(size, dtype=np.uint8)
        self.reward = np.zeros(size, dtype=np.float32)
        self.is_done = np.zeros(size, dtype=np.uint8)
        self.ptr, self.size, self.max_size = 0, 0, size

    def save(self, status, action, reward, next_status, is_done):
        self.current_status[self.ptr] = status
        self.next_status[self.ptr] = next_status
        self.action[self.ptr] = action
        self.reward[self.ptr] = reward
        self.is_done[self.ptr] = is_done
        self.ptr = (self.ptr+1) % self.max_size
        self.size = min(self.size+1, self.max_size)

    def sample_batch(self, batch_size = 32):
        # generate 32 indexes
        index = np.random.randint(0, self.size, size=batch_size)
        return dict(s=self.current_status[index],
                    s2=self.next_status[index],
                    a=self.action[index],
                    r=self.reward[index],
                    d=self.is_done[index])
