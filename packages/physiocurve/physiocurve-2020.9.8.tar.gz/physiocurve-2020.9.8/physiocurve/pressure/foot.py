import numpy as np
from numba import njit


@njit(cache=True, parallel=True)
def findPressureFeet(values, samplerate):
    fstderiv = np.diff(values, 1)
    fstderiv = np.append(fstderiv, np.nan)
    sndderiv = np.diff(fstderiv, 1)
    sndderiv = np.append(sndderiv, np.nan)
    sndderiv = sndderiv * (fstderiv > 0)
    risingStarts, risingStops = sliding_search_zois(sndderiv, samplerate)
    outlen = min([len(x) for x in (risingStarts, risingStops)])
    outarr = np.empty(outlen, dtype=np.int64)
    for i in range(outlen):
        start = risingStarts[i]
        stop = risingStops[i]
        outarr[i] = start + np.argmax(sndderiv[start:stop])
    return outarr


# @njit(cache=True, parallel=True)
@njit(cache=True)
def roll_with(a, w, f, center=True):
    n = len(a) - w + 1
    # buf = np.empty(n)
    buf = np.empty(len(a))
    for i in range(n):
        buf[i] = f(a[i : i + w])
    return buf


# should be implemented with partial application but not supported by numba
# @njit(cache=True, parallel=True)
@njit(cache=True)
def roll_quant7(a, w, center=True):
    n = len(a) - w + 1
    # buf = np.empty(n)
    buf = np.empty(len(a))
    for i in range(n):
        buf[i] = np.nanquantile(a[i : i + w], 0.7)
    return buf


@njit(cache=True, parallel=True)
def sliding_search_zois(a, samplerate, sumcoef=4, quantcoef=3):
    winsum = samplerate // sumcoef
    winquant = int(samplerate * quantcoef)
    sq = a ** 2
    integral = roll_with(sq, winsum, np.nansum)
    thres = roll_quant7(integral, winquant)
    risings = integral > thres
    risingvar = np.diff(risings.astype(np.int8))
    risingStarts = np.flatnonzero(risingvar > 0)
    risingStops = np.flatnonzero(risingvar < 0)
    risingStops = risingStops[risingStops > risingStarts[0]]
    return (risingStarts, risingStops)


@njit(cache=True, parallel=True)
def calc_heartrate(feetidx, samplerate):
    dfeet = np.diff(feetidx)
    dfeet_s = dfeet / samplerate
    # Result in beats per minute
    return 60 / dfeet_s


if __name__ == '__main__':
    import pandas as pd
    import matplotlib.pyplot as plt

    infile = '../testdata/pletho_test.parquet'
    df = pd.read_parquet(infile)

    pleth = df['Pleth'].dropna()
    pleth.index = pleth.index.astype(np.int64)
    feet = findPressureFeet(pleth.values, 125)

    plt.plot(pleth.index, pleth.values)
    plt.scatter(feet.index, feet.values)
    plt.show()
