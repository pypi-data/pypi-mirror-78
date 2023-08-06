import numpy as np

from physiocurve.common import truncatevecs


def findFlowCycles(curve):
    series = curve.series
    bincycles = (series > series.min()).astype(int)
    (idxstarts,) = (bincycles.diff().shift(-1) > 0).nonzero()
    (idxstops,) = (bincycles.diff() < 0).nonzero()
    cycleStarts = series.iloc[idxstarts]
    cycleStops = series.iloc[idxstops]

    # Handle the case where we start within a cycle
    try:
        cycleStops = cycleStops[cycleStops.index > cycleStarts.index[0]]
    except IndexError as e:
        raise TypeError(f'No cycle detected: {e}')

    return (cycleStarts.index, cycleStops.index)


def findFlowCyclesNp(values):
    bincycles = values > np.min(values)
    diff = np.diff(bincycles)
    cycle_starts = np.flatnonzero(diff > 0)
    cycle_stops = np.flatnonzero(diff < 0)

    # Handle the case where we start within a cycle
    for n, s in enumerate(cycle_stops):
        if s > cycle_starts[0]:
            break

    return truncatevecs((cycle_starts, cycle_stops[n:]))
