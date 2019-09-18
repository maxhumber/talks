import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('max_bike_data.csv')
df['time'] = pd.to_datetime(df['time'])

for col in df:
    percent_missing = df[df[col].isnull() == True].shape[0] / df.shape[0]
    print(f'percent missing for column {col}: {percent_missing:.3f}')

df = df.dropna()

TARGET = 'drop_off'

y = df[TARGET].values
X = df.drop(TARGET, axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
