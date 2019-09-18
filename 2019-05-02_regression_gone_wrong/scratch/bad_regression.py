import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt

df = pd.read_csv('data/skaters.csv')
columns = ['name', 'age', 'position', 'goals', 'assists', 'plus_minus', 'shots_on_goal', 'blocks', 'hits']
df = df[columns].dropna()

y = df['goals']
X = df[['age', 'assists', 'plus_minus', 'shots_on_goal', 'blocks', 'hits']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
y_hat = model.predict(X_test)

r2_score(y_test, y_hat)
mean_absolute_error(y_test, y_hat)

plt.figure(figsize=(8, 8))
plt.scatter(y_test, y_hat, alpha=1/5)
plt.plot([0, 50], [0, 50], c='r')
