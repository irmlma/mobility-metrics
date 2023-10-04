import argparse

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely import wkt


import matplotlib.pyplot as plt
import powerlaw

from mobmetric import radius_gyration

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "method",
        default="count",
        nargs="?",
        choices=["duration", "count"],
        help="Method for calculating radius of gyration (default: %(default)s)",
    )
    args = parser.parse_args()

    sp = pd.read_csv("data/input/depr.csv", index_col="index")
    sp["geometry"] = sp["geometry"].apply(wkt.loads)
    sp = gpd.GeoDataFrame(sp, geometry="geometry", crs="EPSG:4326")

    rg = radius_gyration(sp, method=args.method, print_progress=True)

    # transform to km
    rg = rg / 1000

    # fit power law
    fit = powerlaw.Fit(rg, xmin=1)

    # plotting
    powerlaw.plot_pdf(rg)
    fit.power_law.plot_pdf(linestyle="--", label="powerlaw fit")
    fit.truncated_power_law.plot_pdf(linestyle="--", label="truncated power law")
    fit.lognormal.plot_pdf(linestyle="--", label="lognormal fit")

    plt.legend(prop={"size": 13})

    plt.xlabel("$Rg$ (km)", fontsize=16)
    plt.ylabel("$P(Rg)$", fontsize=16)

    plt.show()
