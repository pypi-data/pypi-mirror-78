from physiocurve.flow import flow
from physiocurve.common import estimate_samplerate


class Flow:
    def __init__(self, values, samplerate):
        self._values = values
        self._samplerate = samplerate
        self._starts = None
        self._stops = None

    @classmethod
    def from_pandas(cls, series, samplerate=None):
        if samplerate is None:
            samplerate = estimate_samplerate(series)
        return cls(series.to_numpy(), samplerate)

    @property
    def samplerate(self):
        return self._samplerate

    @property
    def start_offsets(self):
        if self._starts is None:
            self._starts, self._stops = flow.findFlowCyclesNp(self._values)
        return self._starts

    @property
    def stop_offsets(self):
        if self._stops is None:
            self._starts, self._stops = flow.findFlowCyclesNp(self._values)
        return self._stops
