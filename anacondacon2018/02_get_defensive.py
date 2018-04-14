import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer

df = pd.read_csv('max_bike_data.csv')
df['time'] = pd.to_datetime(df['time'])

for col in df:
    percent_missing = df[df[col].isnull() == True].shape[0] / df.shape[0]
    print(f'percent missing for column {col}: {percent_missing:.3f}')

df = df.dropna()
# df = df[df['drop_off'].notnull()]

TARGET = 'drop_off'

y = df[TARGET].values
X = df.drop(TARGET, axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

from sklearn.preprocessing import LabelBinarizer
lb = LabelBinarizer()
lb.fit_transform(X_train.pick_up)

lb.transform(['home'])

lb.transform([np.nan])

# SKP

from sklearn_pandas import DataFrameMapper, CategoricalImputer

mapper = DataFrameMapper([
    ('time', None),
    ('pick_up', None),
    ('last_drop_off', CategoricalImputer()),
    ('last_pick_up', CategoricalImputer())
])

mapper.fit(X_train)

mapper.transform(
    pd.DataFrame({
        'pick_up': ['work'],
        'time': [pd.Timestamp(2018, 4, 1, 9, 30)],
        'last_drop_off': [None],
        'last_pick_up': [None]
    })
)

# SKP chaining

mapper = DataFrameMapper([
    # ('time', None),
    ('pick_up', LabelBinarizer()),
    ('last_drop_off', [CategoricalImputer(), LabelBinarizer()]),
    ('last_pick_up', [CategoricalImputer(), LabelBinarizer()])
])

mapper.fit_transform(X_train)

mapper.transform(
    pd.DataFrame({
        'pick_up': ['work'],
        'time': [pd.Timestamp(2018, 4, 1, 9, 30)],
        'last_drop_off': [None],
        'last_pick_up': [None]
    })
)

# custom transformer

from sklearn.base import TransformerMixin

class DateEncoder(TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        dt = X.dt
        return pd.concat([
            dt.month, dt.dayofweek, dt.hour
        ], axis=1)

X = pd.DataFrame({'time': [pd.Timestamp(2018, 4, 1, 9, 30)]})

de = DateEncoder()
de.fit(X.time)
de.transform(X.time)

# SKP with the transformer

mapper = DataFrameMapper([
    ('time', DateEncoder(), {'input_df': True}),
    ('pick_up', LabelBinarizer()),
    ('last_drop_off', [CategoricalImputer(), LabelBinarizer()]),
    ('last_pick_up', [CategoricalImputer(), LabelBinarizer()])
])

mapper.fit_transform(X_train)

mapper.transform(
    pd.DataFrame({
        'pick_up': ['work'],
        'time': [pd.Timestamp(2018, 4, 1, 9, 30)],
        'last_drop_off': ['home'],
        'last_pick_up': ['fljkkflkjflsanfsadas']
    })
)
