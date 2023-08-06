from .__version__ import __version__  # noqa: F401

from . import datasets  # noqa: F401
from . import vignettes  # noqa: F401
import matplotlib.pyplot as plt
import time
import numpy as np


def vis_binary_classification(model, X, y, epochs=200):
    plt.ion()
    min = np.min(X)-0.2
    max = np.max(X)+0.2
    x1 = np.linspace(min, max, 100)
    grid = np.array([(x, y) for x in x1 for y in x1])
    fig = plt.figure()
    ax = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    real_x = x1
    real_y = x1
    dx = (real_x[1]-real_x[0])/2.
    dy = (real_y[1]-real_y[0])/2.
    extent = [real_x[0]-dx, real_x[-1]+dx, real_y[0]-dy, real_y[-1]+dy]

    ax.set_xlim([min, max])
    ax.set_ylim([min, max])
    ax2.set_xlim([0, epochs])
    line1, = ax2.plot([], [], 'r-')
    # first image

    output = np.array(model(grid))
    img = ax.imshow(output.reshape(100, 100), extent=extent)

    ax.scatter(X[:, 0], X[:, 1], c=y, edgecolor='black')

    losses = []
    model = model
    for x in range(epochs):
        model.fit(X, y, epochs=1, verbose=0)
        output = np.array(model(grid))
        arr_output = output.reshape(100, 100)
        img.set_data(arr_output)
        loss = model.evaluate(X, y, verbose=0)
        if isinstance(loss, list):
            loss = loss[0]
        losses.append(loss)
        line1.set_data(list(range(x+1)), losses)
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.025)
    plt.ioff()
    plt.show()
