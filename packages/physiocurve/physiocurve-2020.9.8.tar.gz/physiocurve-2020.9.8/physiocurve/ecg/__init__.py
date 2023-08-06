from physiocurve.ecg.wrapper import Ecg


if __name__ == '__main__':
    import pandas as pd

    # import matplotlib.pyplot as plt

    infile = '../../testdata/ecg_test.parquet'
    df = pd.read_parquet(infile)
    print(df.columns)
    ecg = df['V'].dropna()

    e = Ecg.from_pandas(ecg)
    print(e.samplerate)
    # print(e.rwave_offsets)
    rwaves = ecg.iloc[e.rwave_offsets]
    print(rwaves)
