import pandas as pd
import numpy as np
from fire import Fire

def _predict(X):
    return np.where(X.time.dt.hour <= 10, 'work', 'home')

def predict(file):
    df = pd.read_csv(file)
    df['time'] = pd.to_datetime(df['time'])
    df = df[df['drop_off'].notnull()]
    output = pd.DataFrame({
        'time': df.time,
        'pick_up': df.pick_up,
        'drop_off': df.drop_off,
        'predicted_drop_off': _predict(df)})
    output.to_csv('output.csv', index=False)
    print('success!')

if __name__ == '__main__':
    Fire()
