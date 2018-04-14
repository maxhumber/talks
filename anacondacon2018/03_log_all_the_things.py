import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from sklearn.base import TransformerMixin
from sklearn_pandas import DataFrameMapper, CategoricalImputer

df = pd.read_csv('max_bike_data.csv')
df['time'] = pd.to_datetime(df['time'])
df = df.dropna()

TARGET = 'drop_off'
y = df[TARGET].values
X = df.drop(TARGET, axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

class DateEncoder(TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        dt = X.dt
        return pd.concat([
            dt.month, dt.dayofweek, dt.hour
        ], axis=1)

mapper = DataFrameMapper([
    ('time', DateEncoder(), {'input_df': True}),
    ('pick_up', LabelBinarizer()),
    ('last_drop_off', [CategoricalImputer(), LabelBinarizer()]),
    ('last_pick_up', [CategoricalImputer(), LabelBinarizer()])
])

mapper.fit_transform(X_train)

# cerberus introduction

from cerberus import Validator

schema = {
    'time': {'type': 'datetime', 'nullable': False},
    'pick_up': {'type': 'string', 'nullable': False, 'allowed': [
        'home', 'work', 'climbing', 'west_core', 'downtown_core', 'other', 'art']
    },
    'last_drop_off': {'type': 'string', 'nullable': True},
    'last_pick_up': {'type': 'string', 'nullable': True}
}

example = {
    'pick_up': 'work',
    'time': pd.Timestamp(2018, 4, 1, 9, 30),
    'last_drop_off': 'home',
    'last_pick_up': 'west_core'
}

v = Validator()
v.validate(example, schema)
v.errors

# a failing example

bad_example = {
    'pick_up': 'sakjfnskffs',
    'time': [],
    'last_drop_off': 42,
    'last_pick_up': 'west_core'
}

v.validate(bad_example, schema)
v.errors

# proto-pandas extension example

df = pd.DataFrame({
    'pick_up': ['work'],
    'time': [pd.Timestamp(2018, 4, 1, 9, 30)],
    'last_drop_off': ['home'],
    'last_pick_up': ['downtown_core']
})

df_list = df.to_dict(orient='list')
# for k, v in schema.items():
#     schema[k] = {'type': 'list', 'schema': v}

# pandas validator

from cerberus import Validator
from copy import deepcopy

class PandasValidator(Validator):

    def validate(self, document, schema, update=False, normalize=True):
        document = document.to_dict(orient='list')
        schema = self.transform_schema(schema)
        super().validate(document, schema, update=update, normalize=normalize)

    def transform_schema(self, schema):
        schema = deepcopy(schema)
        for k, v in schema.items():
            schema[k] = {'type': 'list', 'schema': v}
        return schema

schema = {
    'time': {'type': 'datetime', 'nullable': False},
    'pick_up': {'type': 'string', 'nullable': False, 'allowed': [
        'home', 'work', 'climbing', 'west_core', 'downtown_core', 'other', 'art']
    },
    'last_drop_off': {'type': 'string', 'nullable': True},
    'last_pick_up': {'type': 'string', 'nullable': True}
}

df = pd.DataFrame({
    'pick_up': ['work'],
    'time': [None],
    'last_drop_off': ['home'],
    'last_pick_up': ['downtown_core']
})

pv = PandasValidator()
pv.validate(df, schema)
pv.errors

# cerberus with rollbar example

import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import rollbar

ROLLBAR_KEY = os.environ.get('ROLLBAR')
rollbar.init(ROLLBAR_KEY)

pv = PandasValidator()
pv.validate(df, schema)
pv.errors

if pv.errors:
    rollbar.report_message(f'Got a schema error: {str(pv.errors)}', 'warning')
