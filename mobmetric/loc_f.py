def location_frquency(sp):
    """Location visit frquency for datasets

    Parameters
    ----------
    sp : Geodataframe
        Staypoints with column "location_id" and "user_id".

    Returns
    -------
    s: list
        the ranked visit frquency.

    References
    ----------
    [1] Gonzalez, M. C., Hidalgo, C. A., & Barabasi, A. L. (2008). Understanding individual human mobility patterns. Nature, 453(7196), 779-782.

    """

    # get visit times per user and location
    freq = sp.groupby(["user_id", "location_id"], as_index=False).size()
    # get the rank of locations per user
    freq["visitRank"] = freq.groupby("user_id")["size"].rank(ascending=False, method="first")
    # get the average visit freqency for every rank
    pLoc = freq.groupby("visitRank")["size"].mean().values

    # normalize
    pLoc = pLoc / pLoc.sum()

    return pLoc
