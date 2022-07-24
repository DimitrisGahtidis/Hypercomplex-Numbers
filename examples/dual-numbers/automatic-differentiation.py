import sys
import os

sys.path.append(os.path.abspath('.'))

from modules.numbers import dnum as dn
# from modules.functions import *
import numpy as np
import scipy.sparse as sp
import matplotlib.pyplot as plt
from matplotlib import animation
import time

def sigmoid(x):
    if hasattr(x, '__iter__'):
        for i, item in enumerate(x):
            x[i] = sigmoid(item)
        return x
    else:
        return 1/(1+dn.exp(-x))

def make_matrices(vars, input_layer, hidden_layer, output_layer):
    w1 = vars[:input_layer*hidden_layer]
    w2 = vars[input_layer*hidden_layer:]

    w1 = w1.reshape((input_layer, hidden_layer))
    w2 = w2.reshape((hidden_layer, output_layer))  

    return w1, w2

def forward(x, w1, w2):
    z1 = sigmoid(w1.T@x)
    z2 = sigmoid(w2.T@z1)
    return z2*2-1

def loss(y,pred):
    return (y-pred).T@(y-pred) # v^T*w

def train(backwards, filename, lr, n_inputs, n_in_layer, n_outputs, n_epochs):
    n_weights = n_inputs*n_in_layer+n_in_layer*n_outputs

    dn.backward(backwards)

    x = np.linspace(0, 2*np.pi, num=n_inputs)
    y = np.sin(x)

    x = np.array([dn(value) for value in x])
    y = np.array([dn(value) for value in y])
    # x = dn.split(x)
    # y = dn.split(y)


    weights = np.random.random_sample(n_weights)
    J_weights = sp.csr_matrix(sp.eye(n_weights))
    if backwards:
        weights = np.array([dn(weight, lambda v, r=row: (v*r)) for weight, row in zip(weights, J_weights)])
    else:
        weights = np.array([dn(weight, row) for weight, row in zip(weights, J_weights)])
    # weights = dn.split(weights)

    w1, w2 = make_matrices(weights, n_inputs, n_in_layer, n_outputs)

    X, Y, P = [], [], []
    for epoch in range(n_epochs):
        t = time.perf_counter()
        pred = forward(x, w1, w2)
        results = loss(y,pred)
        X.append(x)
        Y.append(y)
        P.append(pred)

        grad = dn.split(results).im.toarray()[0]
        t = time.perf_counter() - t

        print(f'Epoch: {epoch} Time: {np.round(t,3)} Loss: {np.round(results.re,3)}')
        # print(np.round(grad,1))
        # print(grad)
        weights = weights - lr*grad
        w1, w2 = make_matrices(weights, n_inputs, n_in_layer, n_outputs)

    def animate_function(i):
        x,y,pred = X[i], Y[i], P[i]
        ax.clear()
        ax.plot(dn.split(x).re, dn.split(pred).re)
        ax.plot(dn.split(x).re, dn.split(y).re)
        ax.set_xlim(0,2*np.pi)
        ax.set_ylim(-1,3)
        ax.set_title(f'Epoch: {i}')

    fig = plt.figure()
    ax = plt.axes()

    animation_ = animation.FuncAnimation(fig, animate_function, interval=100, frames=n_epochs)
    # plt.show()

    # Saving the Animation
    folder_path = os.path.abspath(os.path.join('.','animations'))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, filename)
    writergif = animation.PillowWriter(fps=n_epochs/6)
    animation_.save(file_path, writer=writergif)

if __name__ == "__main__":
    lr=0.1
    n_inputs=100
    n_in_layer=4
    n_outputs=100
    n_epochs=20
    print("Starting backward mode...")
    t = time.perf_counter()
    train(backwards=True, filename='backward-mode-auto-diff.gif', lr=lr, n_inputs=n_inputs, n_in_layer=n_in_layer, n_outputs=n_outputs, n_epochs=n_epochs)
    t = time.perf_counter() - t
    print(f'Total time taken: {np.round(t,3)}')
    print("Starting forward mode...")
    t = time.perf_counter()
    train(backwards=False, filename='forward-mode-auto-diff.gif', lr=lr, n_inputs=n_inputs, n_in_layer=n_in_layer, n_outputs=n_outputs, n_epochs=n_epochs)
    t = time.perf_counter() - t
    print(f'Total time taken: {np.round(t,3)}')
