import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam

from replay_buffer import ReplayBuffer

def multi_layer_perception(status_size, action_size, n_hidden_layers=1, hidden_dim=32):
    # input layer
    input_tensor = Input(shape=(status_size,))

    # hidden layers, n_hidden_layers = 1, so there's only 1 hidden_tensor
    hidden_tensor = Dense(hidden_dim, activation='relu')(input_tensor)

    # output layer
    output_tensor = Dense(hidden_dim)(hidden_tensor)

    #make a model
    model = Model(input_tensor, output_tensor)

    # configure the model for training
    # loss = difference between output and target variable (helpful to train neural networks)
    # optimizer reduces model's error by updating parameters of the model
    # mse = Mean Square Error, adam = Adaptive Moment Estimation
    model.compile(loss='mse', optimizer='adam')
    print(model.summary())
    return model

class Agent(object):
    def __init__(self, status_size, action_size, batch_size, number_of_stocks):
        self.status_size = status_size
        self.action_size = action_size
        self.batch_size = batch_size
        self.memory = ReplayBuffer(status_size, size=500)
        self.gamma = 0.95 #discount rate: make infite sum finite
        #decisionmaker is uncertain if next decision is going to end
        #robot optimize discounted sum reward ISO optimize sum reward
        self.epsilon = 1.0 #exploration rate: decision of trying sth new
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model = multi_layer_perception(self.status_size, self.action_size)

    def update_replay_memory(self, status, action, reward, next_status, is_done):
        self.memory.save(status, action, reward, next_status, is_done)

    def action(self, status):
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)
        action_value = self.model.predict(status)
        # generate numpy array of predictions from the parameter status
        return np.argmax(action_value[0])  # returns action
        # argmax returns the position of max value

    def replay(self, batch_size):
        # check if replay buffer contains enough data
        if self.memory.size < batch_size:
            return

        # sample a batch of data from reply memory
        sample = self.memory.sample_batch(batch_size)
        status = sample['s']
        action = sample['a']
        reward = sample['r']
        next_status = sample['s2']
        is_done = sample['d']

        # calculate tentative target: Q(s', a)
        target_nextStatus = reward + (1-is_done) * self.gamma * np.amax(self.model.predict(next_status), axis=1)

        # Q(s,a)
        target_currentStatus = self.model.predict(status)
        target_currentStatus[np.arange(batch_size), action] = target_nextStatus

        self.model.train_on_batch(status, target_currentStatus)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)
