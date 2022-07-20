import sys
import os

sys.path.append(os.path.abspath('.'))

from modules.numbers import Dnum as dn
from modules.functions import *
import numpy as np
import scipy.sparse as sp

def relu(x):
    if hasattr(x, '__iter__'):
        for i, item in enumerate(x):
            x[i] = relu(item)
        return x
    else:
        if x > 0:
            return x
        else:
            return dn(0)

def sigmoid(x):
    if hasattr(x, '__iter__'):
        for i, item in enumerate(x):
            x[i] = sigmoid(item)
        return x
    else:
        return 1/(1+exp(-x))

x = np.arange(50)
x = x/50*2*np.pi
y = np.sin(x)

x = np.array(list(map(lambda x: dn(x), x)))
y = np.array(list(map(lambda x: dn(x), y)))

input_layer, hidden_layer, output_layer = 50, 20, 50

n_weights = input_layer*hidden_layer+hidden_layer*output_layer
weights = np.random.random_sample((1,n_weights))
weights = [dn(value, sp.csr_matrix(sp.eye(1,n_weights, k=i))) for i, value in enumerate(weights[0])]
weights = np.array(weights)

def make_weights(vars, input_layer, hidden_layer, output_layer):
    w1 = vars[:input_layer*hidden_layer]
    w2 = vars[input_layer*hidden_layer:]

    w1 = w1.reshape((input_layer, hidden_layer))
    w2 = w2.reshape((hidden_layer, output_layer))  

    return w1, w2

w1, w2 = make_weights(weights, input_layer, hidden_layer, output_layer)

def forward(x, W1, W2):
    z1 = sigmoid(W1.T@x)
    z2 = W2.T@z1
    return z2

def loss(y,pred):
    return (y-pred).T@(y-pred)

lr = 0.01

print("Starting training...")
for epoch in range(10):
    pred = forward(x, w1, w2)
    results = loss(y,pred)
    print(f'Epoch:{epoch} Loss: {round(dn.split(results).re,5)}')
    weights = weights - lr*sp.csr_matrix(dn.split(results).im()).toarray()[0]

    w1, w2 = make_weights(weights, input_layer, hidden_layer, output_layer)
print(f"Final prediction: {np.round(dn.split(pred).re,2)}")
print(f"Real label: {np.round(dn.split(y).re,2)}")
print("Done")     