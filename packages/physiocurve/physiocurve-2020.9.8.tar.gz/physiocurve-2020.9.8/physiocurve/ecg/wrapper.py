from ecgdetectors import Detectors

from physiocurve.common import estimate_samplerate


class Ecg:
    def __init__(self, values, samplerate):
        self._rwaves = None
        self._values = values
        self._samplerate = samplerate
        self._detectors = Detectors(samplerate)

    @classmethod
    def from_pandas(cls, series, samplerate=None):
        if samplerate is None:
            samplerate = estimate_samplerate(series)
        return cls(series.to_numpy(), samplerate)

    @property
    def samplerate(self):
        return self._samplerate

    @property
    def rwave_offsets(self):
        if self._rwaves is None:
            self._rwaves = self._detectors.christov_detector(self._values)
        return self._rwaves
