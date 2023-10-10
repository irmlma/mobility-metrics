import argparse

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely import wkt


import matplotlib.pyplot as plt
import powerlaw

from mobmetric import radius_gyration, jump_length, location_frquency, wait_time

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "method",
        default="count",
        nargs="?",
        choices=["duration", "count"],
        help="Method for calculating radius of gyration (default: %(default)s)",
    )
    parser.add_argument(
        "metric",
        default="rg",
        nargs="?",
        choices=["rg", "locf", "jump", "wait"],
        help="Metric to calculate (default: %(default)s)",
    )

    args = parser.parse_args()

    sp = pd.read_csv("data/input/dtepr.csv", index_col="index")
    sp["geometry"] = sp["geometry"].apply(wkt.loads)
    sp = gpd.GeoDataFrame(sp, geometry="geometry", crs="EPSG:4326")

    if args.metric == "jump":
        metric = jump_length(sp)
        xlabel = "$\Delta r\,(m)$"
        ylabel = "$P(\Delta r)$"
        xmin = 1

    elif args.metric == "rg":
        metric = radius_gyration(sp, method=args.method, print_progress=True)
        # transform to km
        metric = metric / 1000

        xlabel = "$Rg$ (km)"
        ylabel = "$P(Rg)$"
        xmin = 1

    elif args.metric == "wait":
        metric = wait_time(sp)

        xlabel = "$\Delta t\,(hour)$"
        ylabel = "$P(\Delta t)$"
        xmin = 0.1

    elif args.metric == "locf":
        loc_freq = location_frquency(sp)

        xlabel = "$f_k$"
        ylabel = "$k$"

    else:
        raise AttributeError(
            f"Metric unknown. Please check the input arguement. We only support 'rg', 'locf', 'jump'. You passed {args.method}"
        )

    plt.figure(figsize=(8, 5))

    if args.metric == "jump" or args.metric == "rg" or args.metric == "wait":
        # fit power law
        fit = powerlaw.Fit(metric, xmin=xmin)

        # plotting
        powerlaw.plot_pdf(metric, label="data")
        fit.power_law.plot_pdf(linestyle="--", label="powerlaw fit")
        fit.truncated_power_law.plot_pdf(linestyle="--", label="truncated power law")
        fit.lognormal.plot_pdf(linestyle="--", label="lognormal fit")
    else:
        n = np.arange(len(loc_freq)) + 1
        plt.plot(n, np.power(n, -1.0) / 4, "--", label="$f_k\sim k^{-1}$", color="k")
        plt.plot(n, loc_freq)

        plt.yscale("log")
        plt.xscale("log")

    plt.legend(prop={"size": 13})
    plt.xlabel(xlabel, fontsize=16)
    plt.ylabel(ylabel, fontsize=16)

    plt.show()
