import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score

df = pd.read_csv('max_bike_data.csv')

df['time'] = pd.to_datetime(df['time'])
df = df[df['drop_off'].notnull()]

def predict(X):
    return np.where(X.time.dt.hour <= 10, 'work', 'home')

y_pred = predict(df)
accuracy_score(df['drop_off'], y_pred)

output = pd.DataFrame({'time': df.time, 'pick_up': df.pick_up,
    'drop_off': df.drop_off, 'predicted_drop_off': y_pred})

output.to_csv('output.csv', index=False)
