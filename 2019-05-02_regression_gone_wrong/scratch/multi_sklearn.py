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
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor

skaters = pd.read_csv('data/skaters.csv')
skaters['season_start'] = skaters.season.apply(lambda x: int(x[:4]))
skaters = skaters.query('season_start >= 2007')
skaters['position'] = skaters['position'].apply(lambda x: 'Multiple' if '/' in x else x)
df = skaters.copy()


Y_COLUMNS = ['goals', 'assists', 'plus_minus', 'shots_on_goal', 'blocks', 'hits']
# X_COLUMNS = ['name', 'position', 'age'] + Y_COLUMNS
X_COLUMNS = ['position', 'age'] + Y_COLUMNS

# setup data for prediction
Y = df.groupby('id')[Y_COLUMNS].shift(-1)
X = df[X_COLUMNS]
X = X[~pd.isnull(Y).any(axis=1)]
Y = Y.dropna()
Y = Y.reset_index(drop=True)
X = X.reset_index(drop=True)

X_train, X_test, Y_train, Y_test = (
    train_test_split(X, Y, test_size=0.2, random_state=42)
)

mapper = DataFrameMapper([
    (['age'], [SimpleImputer(), PolynomialFeatures(include_bias=False)]),
    (['position'], [CategoricalImputer(), LabelBinarizer()]),
    (['goals'], SimpleImputer()),
    (['assists'], SimpleImputer()),
    (['plus_minus'], SimpleImputer()),
    (['shots_on_goal'], SimpleImputer()),
    (['blocks'], SimpleImputer()),
    (['hits'], SimpleImputer())
], df_out=False)

Z_train = mapper.fit_transform(X_train)
Z_test = mapper.transform(X_test)

from sklearn.linear_model import LinearRegression
multi_model = MultiOutputRegressor(LinearRegression())
multi_model.fit(Z_train, Y_train)
pd.DataFrame(Z_test).iloc[:, 8:].head()
pd.DataFrame(multi_model.predict(Z_test)).head()
multi_model.score(Z_test, Y_test)
