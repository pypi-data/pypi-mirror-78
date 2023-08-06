from physiocurve.pressure.foot import findPressureFeet, findPressureFeet
from physiocurve.pressure.incycle import (
    find_dia_sys,
    find_dicrotics,
    findPressureFull,
)

from physiocurve.pressure.wrapper import Pressure


if __name__ == '__main__':
    import pandas as pd
    import matplotlib.pyplot as plt

    infile = '../../testdata/pressure_test.parquet'
    df = pd.read_parquet(infile)
    data = df['ART-125.0Hz'].dropna()

    p = Pressure.from_pandas(data)
    feet = data.iloc[p.feet]
    # dics = data.iloc[p.dicrotic_offsets]
    sqi = p.calc_sqi()
    ssqi = pd.Series(p.calc_sqi(), index=data.index[p.diastolic_offsets])
    ssqi = ssqi[p.diastolic_offsets != 0]

    plt.plot(data.index, data.values, '-')
    plt.plot(ssqi.index, ssqi.values * 100, '-')
    plt.plot(feet.index, feet.values, 'o')
    # plt.plot(dics.index, dics.values, 'o')
    plt.show()
