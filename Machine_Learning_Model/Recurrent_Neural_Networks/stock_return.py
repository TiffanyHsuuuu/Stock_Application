
from tensorflow.keras.layers import Input, LSTM, GRU, SimpleRNN, Dense, GlobalMaxPool1D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import SGD, Adam

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


df = pd.read_csv('AAPL_data.csv', sep=r'\t', engine='python')

series = df['4. close'].values.reshape(-1,1)

# Normalize the data
scaler = StandardScaler()
scaler.fit(series[:len(series)//2])
series = scaler.transform(series).flatten()

# Build dataset
T = 10 #use T past values to predict the next value
D = 1
X = []
Y = []
for t in range(len(series) - T):
    x = series[t:t+T]
    X.append(x)
    y = series[t+T]
    Y.append(y)
X = np.array(X).reshape(-1, T, 1) #data shall be N*T*D
Y = np.array(Y)
N = len(X)
print("X.shape", X.shape, "Y.shape", Y.shape)

# try autoregressive RNN model
i = Input(shape=(T,1))
x = LSTM(5)(i)
x = Dense(1)(x)
model = Model(i,x)
model.compile(
    loss = 'mse',
    optimizer = Adam(lr=0.1),
)

# train RNN
r = model.fit(
    X[:-N//2], Y[:-N//2],
    epochs=80,
    validation_data=(X[-N//2:], Y[-N//2:]),
)

# plot loss per iteration
plt.plot(r.history['loss'], label='loss from test data')
plt.plot(r.history['val_loss'], label='loss from training data')
plt.legend()
plt.show()

# one-step forecast using true targets
predict = model.predict(X)
predictions = predict[:,0]
plt.plot(Y, label='Targets')
plt.plot(predictions, label='Predictions')
plt.legend()
plt.show()

file = np.asarray(Y)
file.tofile('targets.csv', sep=',', format='%10.5f')

file = np.asarray(predictions)
file.tofile('predictions.csv', sep=',', format='%10.5f')
