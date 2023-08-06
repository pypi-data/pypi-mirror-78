from physiocurve.pressure import foot, incycle
from physiocurve.common import estimate_samplerate


class Pressure:
    def __init__(self, values, samplerate):
        self._values = values
        self._samplerate = samplerate
        self._feet = None
        self._dia = None
        self._sys = None
        self._dic = None
        self._means = None
        self._hr = None

    @classmethod
    def from_pandas(cls, series, samplerate=None):
        if samplerate is None:
            samplerate = estimate_samplerate(series)
        return cls(series.to_numpy(), samplerate)

    @property
    def samplerate(self):
        return self._samplerate

    @property
    def feet(self):
        if self._feet is None:
            self._feet = foot.findPressureFeet(self._values, self._samplerate)
        return self._feet

    @property
    def diastolic_offsets(self):
        if self._dia is None:
            self._dia, self._sys = incycle.find_dia_sys(
                self._values, self._samplerate, self.feet
            )
        return self._dia

    @property
    def systolic_offsets(self):
        if self._dia is None:
            self._dia, self._sys = incycle.find_dia_sys(
                self._values, self._samplerate, self.feet
            )
        return self._sys

    @property
    def dicrotic_offsets(self):
        if self._dic is None:
            self._dic = incycle.find_dicrotics(
                self._values, self.diastolic_offsets, self.systolic_offsets
            )
        return self._dic

    @property
    def means(self):
        if self._means is None:
            self._means = incycle.calc_means(self._values, self.diastolic_offsets)
        return self._means

    @property
    def heartrate(self):
        if self._hr is None:
            self._hr = foot.calc_heartrate(self.feet, self._samplerate)
        return self._hr

    def calc_sqi(self):
        return incycle.calc_quality_index(
            self._values,
            self.diastolic_offsets,
            self.systolic_offsets,
            self.means,
            self.heartrate,
            self._samplerate,
        )
