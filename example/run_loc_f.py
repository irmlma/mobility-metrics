import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from mobmetric import location_frquency

if __name__ == "__main__":
    sp = pd.read_csv("data/input/ipt.csv", index_col="index")
    loc_freq = location_frquency(sp)

    fig, ax = plt.subplots(1, 1, figsize=(8, 5))

    n = np.arange(len(loc_freq)) + 1
    plt.plot(n, np.power(n, -1.0) / 4, "--", label="$f_k\sim k^{-1}$", color="k")
    plt.plot(n, loc_freq)

    plt.legend(prop={"size": 14}, title_fontsize=18, loc=1)
    plt.ylabel("$f_k$", fontsize=16)
    plt.xlabel("$k$", fontsize=16)
    plt.yscale("log")
    plt.xscale("log")

    plt.show()
