from physiocurve.pressure import Pressure


class PPG(Pressure):
    def __init__(self, values, samplerate):
        super().__init__(values, samplerate)

    def calc_sqi(self):
        raise NotImplementedError
