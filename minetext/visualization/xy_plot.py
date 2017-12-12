import numpy as np
import matplotlib.pyplot as plt


def xy_plot(x, y, xlabel, ylabel, title, save_dir):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(np.array(x), np.array(y))
    plt.savefig(save_dir)


def generate_xy_elbow_plot(elbow_result, save_dir):
    title = "Elbow method result"
    xlabel = "K clusters"
    x = list(elbow_result.keys())
    ylabel = "Sum of Squared Errors (SSE)"
    y = list(elbow_result.values())
    xy_plot(x, y, xlabel, ylabel, title, save_dir)

if __name__ == "__main__":
    pass
