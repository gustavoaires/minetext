import numpy as np
import matplotlib.pyplot as plt


def xy_plot(x, y, xlabel, ylabel, title, save_dir):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(np.array(x), np.array(y))
    plt.savefig(save_dir)

if __name__ == "__main__":
    pass
