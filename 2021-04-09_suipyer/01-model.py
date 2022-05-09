import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import coremltools as ct

# load
df = pd.read_csv('data/games.csv')

# split
target = 'rating'
predictors = [
    'time', 'age', 'complexity', 'abstract',
    'childrens', 'customizable', 'family', 'party',
    'strategy', 'thematic', 'wargames'
]
y = df[target]
X = df[predictors]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

# model
model = LinearRegression()
model.fit(X_train, y_train)
print(model.score(X_train, y_train), model.score(X_test, y_test))

# convert
coreml_model = ct.converters.sklearn.convert(model, predictors, target)
coreml_model.save('models/BoardGameRegressor1.mlmodel')
