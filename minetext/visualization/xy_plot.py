import numpy as np
import matplotlib.pyplot as plt


def xy_plot(x, y, save_dir):
    plt.plot(np.array(x), np.array(y))
    plt.savefif(save_dir)

if __name__ == "__main__":
    pass
