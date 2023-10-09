import argparse
import numpy as np
import pandas as pd
import geopandas as gpd
import datetime

import scipy.stats as stats

from shapely import wkt
import matplotlib.pyplot as plt

from mobmetric import mobility_motifs


def _transfer_time_to_absolute(df, start_time):
    duration_arr = df["duration"].to_list()[:-1]
    duration_arr.insert(0, 0)
    timedelta_arr = np.array([datetime.timedelta(hours=i) for i in np.cumsum(duration_arr)])

    df["started_at"] = timedelta_arr + start_time
    df["finished_at"] = df["started_at"] + pd.to_timedelta(df["duration"], unit="hours")

    return df


def _get_motifs_proportion(df):
    return (len(df["class"]) - df["class"].isna().sum()) / len(df["class"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "proportion_filter",
        default=0.005,
        type=float,
        nargs="?",
        help="Proportion filter for considering day graphs as motifs (default: %(default)s)",
    )
    parser.add_argument(
        "time_format",
        default="relative",
        nargs="?",
        choices=["absolute", "relative"],
        help="Dataset (default: %(default)s)",
    )

    args = parser.parse_args()

    # read and preprocess
    if args.time_format == "absolute":
        sp = pd.read_csv("data/input/sp.csv", index_col="id")

        geom_name = "geom"
    elif args.time_format == "relative":
        sp = pd.read_csv("data/input/dtepr.csv", index_col="index")

        geom_name = "geometry"
    else:
        raise AttributeError(
            f"time_format unknown. Please check the input arguement. We only support 'absolute', 'relative'. You passed {args.method}"
        )

    sp[geom_name] = sp[geom_name].apply(wkt.loads)
    sp = gpd.GeoDataFrame(sp, geometry=geom_name, crs="EPSG:4326")

    sp.index.name = "id"
    sp.reset_index(inplace=True)

    if args.time_format == "absolute":
        sp["started_at"] = pd.to_datetime(sp["started_at"], format="mixed", yearfirst=True, utc=True)
        sp["finished_at"] = pd.to_datetime(sp["finished_at"], format="mixed", yearfirst=True, utc=True)
    else:
        # transfer duration to absolut time format for each user
        sp = sp.groupby("user_id", as_index=False).apply(
            _transfer_time_to_absolute, start_time=datetime.datetime(2023, 1, 1, hour=8)
        )
        sp.reset_index(drop=True, inplace=True)

    ## get the motifs
    sp_motifs = mobility_motifs(sp, proportion_filter=args.proportion_filter)

    ## Visualizations
    # get the average proportion
    print(f"Mobility motifs proportion across users: {_get_motifs_proportion(sp_motifs):.3f}")

    # plot the user distribution of all motifs
    plt.figure(figsize=(8, 5))

    # get the user density
    user_motifs_proportion = sp_motifs.groupby("user_id").apply(_get_motifs_proportion).values
    Density = stats.gaussian_kde(user_motifs_proportion)

    # plotting
    x = np.linspace(0, 1, 50)
    plt.plot(x, Density(x))
    plt.xlim([-0.02, 1.02])
    plt.xlabel("Motifs proportion", fontsize=16)
    plt.ylabel("PDF", fontsize=16)

    plt.show()

    # plot the motifs distribution for all user days
    plt.figure(figsize=(8, 5))

    # get the proportion of each motif type for y-axis
    motifs_frq = (
        sp_motifs.dropna(subset="class").groupby(["uniq_visits", "class"], as_index=False).size().reset_index(drop=True)
    )
    motifs_frq["size"] = motifs_frq["size"] / len(sp_motifs)
    # create unique labels for x-axis
    motifs_frq["label"] = (
        motifs_frq["uniq_visits"].astype(int).astype(str) + "_" + motifs_frq["class"].astype(int).astype(str)
    )

    # plotting
    x = np.arange(len(motifs_frq["label"]))
    plt.bar(x=x, height=motifs_frq["size"], tick_label=motifs_frq["label"])
    plt.xlabel("Motifs", fontsize=16)
    plt.ylabel("Proportion", fontsize=16)

    plt.show()
