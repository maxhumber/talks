import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer, StandardScaler
from sklearn_pandas import DataFrameMapper
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
from mord import OrdinalRidge
from matplotlib import pyplot as plt

df = pd.read_csv('data/draft.csv')

categories = [
    'goals',
    'assists',
    'plus_minus',
    'powerplay_points',
    'shots_on_goal',
    'hits',
    'blocks',
    'wins',
    'goals_against_average',
    'saves',
    'save_percentage',
    'shutouts'
]

y = df['adp']
X = df[['position'] + categories]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=5)

mapper = DataFrameMapper(
    [(['position'], LabelBinarizer())],
    default=StandardScaler()
)

Z_train = mapper.fit_transform(X_train)
Z_test = mapper.transform(X_test)

model = LinearRegression()
model.fit(Z_train, y_train)
model.predict(Z_test)[:10]

#!pip install mord
model = OrdinalRidge(fit_intercept=False)
model.fit(Z_train, y_train)
model.predict(Z_test)

compare = pd.DataFrame({
    'y': y_test,
    'yhat': model.predict(Z_test)
})

plt.scatter(compare.y, compare.yhat)
plt.plot([0, 200], [0, 200], c='r')

r2_score(compare.y, compare.yhat)

bias = pd.DataFrame({
    'feature': mapper.transformed_names_,
    'coef': model.coef_
}).sort_values('coef')

bias = bias[~bias.feature.str.contains('position')]
bias
