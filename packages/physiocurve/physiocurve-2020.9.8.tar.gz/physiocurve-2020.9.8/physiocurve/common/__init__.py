import numpy as np


def estimate_samplerate(series):
    # This assumes datetime index
    idx = series.index.astype(np.int64)
    intervals = np.diff(idx)
    # 1e9 to account for ns -> Hz
    fs = 1e9 // np.median(intervals)
    return fs if fs != np.inf else 0


def truncatevecs(vecs):
    # Ensure all vectors have the same length by truncating the end
    maxidx = min(map(len, vecs))
    return [vec[0:maxidx] for vec in vecs]
