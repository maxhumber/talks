import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import LabelBinarizer
from sklearn.impute import SimpleImputer
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn_pandas import DataFrameMapper, CategoricalImputer
from matplotlib import pyplot as plt
import altair as alt

skaters = pd.read_csv('data/skaters.csv')

df = skaters[[
    'name',
    'position',
    'season',
    'age',
    'games_played',
    'time_on_ice_total',
    'goals',
    'shots_on_goal',
    'shots_attempted_total',
]].copy()

# create things to predict
df['goals_next_year'] = df.groupby('name')['goals'].shift(-1)
df['shots_on_goal_next_year'] = df.groupby('name')['shots_on_goal'].shift(-1)
# okay to drop blanks in here
df = df.dropna(subset=['goals_next_year', 'shots_on_goal_next_year'])
# quickly look at year and year+1
plt.scatter(df.goals, df.goals_next_year, alpha=0.2)
# quick naive modeling attempts
truth = df['goals_next_year']
naive = df['goals']
r2_score(truth, naive)
mean_absolute_error(truth, naive)
# train test split on names so there's no target leakage
np.random.seed(42)
names = list(skaters.name.unique())
train_names = np.random.choice(names, size=round(len(names) * 0.80), replace=False)
train = df[df.name.isin(train_names)]
test = df[~df.name.isin(train_names)]
# targets
y_train_goals = train['goals_next_year'].values
y_train_sog = train['shots_on_goal_next_year'].values
y_test_goals = test['goals_next_year'].values
y_test_sog = test['shots_on_goal_next_year'].values
# predictors
X_cols = [
    'age',
    'position',
    'games_played',
    'time_on_ice_total',
    'goals',
    'shots_on_goal',
    'shots_attempted_total',
]
X_train = train[X_cols]
X_test = test[X_cols]
# MapperWrapper!
mapper = DataFrameMapper([
    (['age'], [SimpleImputer(), PolynomialFeatures(include_bias=False), StandardScaler()]),
    (['position'], [CategoricalImputer(), LabelBinarizer()]),
    (['games_played'], [SimpleImputer(), StandardScaler()]),
    (['time_on_ice_total'], [SimpleImputer(), StandardScaler()]),
    (['goals'], [SimpleImputer(), StandardScaler()]),
    (['shots_on_goal'], [SimpleImputer(), StandardScaler()]),
    (['shots_attempted_total'], [SimpleImputer(), StandardScaler()])
    ], df_out=False
)
Z_train = mapper.fit_transform(X_train)
Z_test = mapper.transform(X_test)

# build keras model for goals
from tensorflow.keras import layers
from tensorflow.keras import Input
from tensorflow.keras import models
from tensorflow.keras.models import Model

model = models.Sequential()
model.add(layers.Dense(30, activation='selu', input_dim=Z_train.shape[1]))
model.add(layers.Dense(10, activation='selu'))
model.add(layers.Dropout(0.25))
model.add(layers.Dense(5, activation='selu'))
model.add(layers.Dense(1))
model.compile(optimizer='Nadam', loss='mse', metrics=['mae'])
model.fit(Z_train, y_train_goals, epochs=100, batch_size=10)

import pydot
from tensorflow.keras.utils import plot_model
plot_model(model)

y_hat_test_goals = model.predict(Z_test)
r2_score(y_test_goals, y_hat_test_goals)
mean_absolute_error(y_test_goals, y_hat_test_goals)

plt.figure(figsize=(8, 8))
plt.scatter(y_test_goals, y_hat_test_goals, alpha=1/4)
plt.plot([0, 40], [0, 40], c='red')

# new piece of data
X_test.iloc[0:1].to_dict(orient='list')
# Erik Karlsson from 2017-2018
X_new = pd.DataFrame({
    'age': [28],
    'position': ['D'],
    'games_played': [71],
    'time_on_ice_total': [1899],
    'goals': [9],
    'shots_on_goal': [196],
    'shots_attempted_total': [423]
})
Z_new = mapper.transform(X_new)
model.predict(Z_new)[0][0]

# multi-output model
data_input = Input(shape=(Z_train.shape[1],), dtype='float64', name='last_season')
x = layers.Dense(100, activation='selu')(data_input)
x = layers.Dense(100, activation='selu')(x)
x = layers.Dropout(0.25)(x)
x = layers.Dense(5, activation='selu')(x)
goals_prediction = layers.Dense(1, name='goals')(x)
sog_prediction = layers.Dense(1, name='shots_on_goal')(x)
model = Model(data_input, [goals_prediction, sog_prediction])
model.compile(
    optimizer='Nadam',
    loss={'goals': 'mse', 'shots_on_goal': 'mse'},
    loss_weights={'goals': 10, 'shots_on_goal': 1 / 10},
)
model.fit(Z_train, [y_train_goals, y_train_sog], epochs=20, batch_size=5)

model.predict(Z_test)[1]

plot_model(model)

X_new = pd.DataFrame({
    'age': [28],
    'position': ['D'],
    'games_played': [71],
    'time_on_ice_total': [1899],
    'goals': [9],
    'shots_on_goal': [196],
    'shots_attempted_total': [423]
})
Z_new = mapper.transform(X_new)
model.predict(Z_new)
model.predict(Z_new)[0][0][0]

y_hat_test_goals = model.predict(Z_test)[0][:, 0]
y_hat_test_sog = model.predict(Z_test)[1][:, 0]

preds = pd.DataFrame({
    'goals': y_test_goals,
    'goals_predicted': np.round(y_hat_test_goals),
    'sog': y_test_sog,
    'sog_predicted': y_hat_test_sog,
})

r2_score(preds['goals'], preds['goals_predicted'])
r2_score(preds['sog'], preds['sog_predicted'])
