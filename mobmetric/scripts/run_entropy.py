import argparse
import os

import numpy as np
import pandas as pd
import random
import scipy.stats as stats

import matplotlib.pyplot as plt

from mobmetric import random_entropy, uncorrelated_entropy, real_entropy


def setup_seed(seed):
    """
    fix random seed for reproducing
    """
    np.random.seed(seed)
    random.seed(seed)


if __name__ == "__main__":
    setup_seed(0)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "method",
        default="all",
        nargs="?",
        choices=["random", "uncorrelated", "real", "all"],
        help="Method for calculating mobility entropy (default: %(default)s)",
    )
    parser.add_argument(
        "dataset",
        default="dtepr",
        nargs="?",
        help="Dataset for running (default: %(default)s)",
    )
    args = parser.parse_args()

    sps = pd.read_csv(os.path.join("data", "input", f"{args.dataset}.csv"), index_col="index")

    entropy_result_ls = []
    if args.method == "random":
        entropy_result_ls.append(random_entropy(sps, print_progress=False))
        print(f"Random Entropy: {np.mean(entropy_result_ls[0]):.2f}\t")
    elif args.method == "uncorrelated":
        entropy_result_ls.append(uncorrelated_entropy(sps, print_progress=False))
        print(f"Uncorrelated Entropy: {np.mean(entropy_result_ls[0]):.2f}\t")
    elif args.method == "real":
        entropy_result_ls.append(real_entropy(sps, print_progress=False, n_jobs=-1))
        print(f"Real Entropy: {np.mean(entropy_result_ls[0]):.2f}\t")
    elif args.method == "all":
        entropy_result_ls.append(random_entropy(sps, print_progress=False))
        entropy_result_ls.append(uncorrelated_entropy(sps, print_progress=False))
        entropy_result_ls.append(real_entropy(sps, print_progress=False, n_jobs=-1))
        print(
            f"Random Entropy: {np.mean(entropy_result_ls[0]):.2f},\t Uncorrelated Entropy: {np.mean(entropy_result_ls[1]):.2f},\t Real Entropy: {np.mean(entropy_result_ls[2]):.2f}\t"
        )
    else:
        raise AttributeError(
            f"Method unknown. Please check the input arguement. We only support 'random', 'uncorrelated', 'real', 'all'. You passed {args.method}"
        )

    #
    # ploting
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))

    for entropy in entropy_result_ls:
        density = stats.gaussian_kde(entropy)
        x = np.linspace(0, np.max(entropy) + 0.2, 100)
        ax.plot(x, density(x))

    # plt.legend(prop={"size": 12})
    plt.xlabel("Entropy", fontsize=16)
    plt.ylabel("PDF", fontsize=16)

    plt.show()
