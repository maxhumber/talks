import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from sklearn.pipeline import make_pipeline
from sklearn_pandas import DataFrameMapper, CategoricalImputer
from helpers import DateEncoder

df = pd.read_csv('../max_bike_data.csv')
df['time'] = pd.to_datetime(df['time'])
df = df[(df['pick_up'].notnull()) & (df['drop_off'].notnull())]

TARGET = 'drop_off'
y = df[TARGET].values
X = df.drop(TARGET, axis=1)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

mapper = DataFrameMapper([
    ('time', DateEncoder(), {'input_df': True}),
    ('pick_up', LabelBinarizer()),
    ('last_drop_off', [CategoricalImputer(), LabelBinarizer()]),
    ('last_pick_up', [CategoricalImputer(), LabelBinarizer()])
])

lb = LabelBinarizer()
y_train = lb.fit_transform(y_train)
