import numpy as np
from tqdm import tqdm


from trackintel.geogr.point_distances import haversine_dist


def radius_gyration(sp, print_progress=False, method="count"):
    """
    Radius of gyration for individuals.

    Parameters
    ----------
    sp : Geodataframe
        Staypoints with column "user_id" and geometry.

    print_progress: boolen, default False
        Show per-user progress if set to True.

    method: string, {"duration", "count"}, default "count"
        method to calculate rg. Duration additionally weights each sp with the activity duration.

    Returns
    -------
    pandas Series
        the radius of gyration for individuals.

    References
    ----------
    [1] Gonzalez, M. C., Hidalgo, C. A., & Barabasi, A. L. (2008). Understanding individual human mobility patterns. Nature, 453(7196), 779-782.

    """
    if print_progress:
        tqdm.pandas(desc="User radius of gyration calculation")
        s = sp.groupby("user_id").progress_apply(lambda x: radius_gyration_user(x, method))
    else:
        s = sp.groupby("user_id").apply(lambda x: radius_gyration_user(x, method))

    s.rename("radiusGyration", inplace=True)
    return s


def radius_gyration_user(sp_user, method):
    """
    User level radius of gyration calculation, see radius_gyration() for details.

    Parameters
    ----------
    sp_user : Geodataframe
        The staypoints from an individual, should contain "geometry".

    method: string, {"duration", "count"}, default "count"
        method to calculate rg. Duration additionally weights each sp with the activity duration.
    Returns
    -------
    float
        the radius of gyration of the individual
    """
    sp_user["lat"] = sp_user["geometry"].y
    sp_user["lng"] = sp_user["geometry"].x
    lats_lngs = sp_user[["lat", "lng"]].values

    if method == "duration":
        durs = sp_user[["duration"]].values

        center_of_mass = np.sum([lat_lng * dur for lat_lng, dur in zip(lats_lngs, durs)], axis=0) / np.sum(durs)
        inside = [
            dur * (haversine_dist(lng, lat, center_of_mass[-1], center_of_mass[0]) ** 2.0)
            for (lat, lng), dur in zip(lats_lngs, durs)
        ]

        rg = np.sqrt(np.sum(inside) / sp_user["duration"].sum())
    elif method == "count":
        center_of_mass = np.mean(lats_lngs, axis=0)
        rg = np.sqrt(
            np.mean([haversine_dist(lng, lat, center_of_mass[-1], center_of_mass[0]) ** 2.0 for lat, lng in lats_lngs])
        )
    else:
        raise AttributeError(
            f"Method unknown. Please check the input arguement. We only support 'duration', 'count'. You passed {method}"
        )
    return rg
