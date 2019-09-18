import numpy as np
import pandas as pd
import statsmodels.api as sm

import matplotlib.pyplot as plt
%matplotlib inline

df = pd.read_csv('data/games.csv')
last_year = df.query('season == "2017-18"')

home = df.groupby('home').mean().reset_index().rename(
    columns={'home_goals': 'home_for', 'away_goals': 'home_against'})
away = df.groupby('away').mean().reset_index().rename(
    columns={'home_goals': 'away_against', 'away_goals': 'away_for'})

this_year = df.query('season == "2018-19"')

df = pd.merge(this_year, home, how='left', on='home')
df = pd.merge(df, away, how='left', on='away')

df['home_for*away_against'] = df['home_for'] * df['away_against']
df['away_for*home_against'] = df['away_for'] * df['home_against']
df['goals_total'] = df['home_goals'] + df['away_goals']

y = df['goals_total']
X = df[[
    'home_for', 'home_against', 'away_against', 'away_for',
    'home_for*away_against', 'away_for*home_against'
]]

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)

from sklearn.metrics import r2_score, mean_absolute_error
y_hat = model.predict(X_test)

plt.scatter(y_test, y_hat, alpha=1/10);
r2_score(y_test, y_hat)

# quickly find the mean and variance of the data
np.var(y)
np.mean(y)

# Set up Xi and try to do vanilla statsmodels
X_train_i = sm.add_constant(X_train)
glm_poi = sm.GLM(y_train, X_train_i, family=sm.families.Poisson())
glm_poi = glm_poi.fit()
glm_poi.summary()

y_hat = glm_poi.predict(sm.add_constant(X_test))
plt.scatter(y_test, y_hat, alpha=1/10);
r2_score(y_test, y_hat)


# try to use sklearn
# https://scikit-learn.org/stable/developers/contributing.html#rolling-your-own-estimator
from sklearn.base import BaseEstimator

class PoissonRegression(BaseEstimator):
    def __init__(self, fit_intercept=True):
        self.fit_intercept = fit_intercept

    def fit(self, X, y):
        if self.fit_intercept:
            X = sm.add_constant(X)
        self.model = sm.GLM(y, X, family=sm.families.Poisson()).fit()
        if self.fit_intercept:
            self.coef_ = self.model.params[1:]
            self.intercept_ = self.model.params[0]
        else:
            self.coef_ = self.model.params
        return self

    def predict(self, X):
        if self.fit_intercept:
            X = sm.add_constant(X)
        return self.model.predict(X)

pr = PoissonRegression()
pr.fit(X_train, y_train)
pr.predict(X_test)[:10]

y_hat = pr.predict(X_test)

plt.scatter(y_test, y_hat, alpha=1/10)
