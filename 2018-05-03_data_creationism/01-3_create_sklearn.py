import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_classification
import altair as alt


import numpy as np
import pandas as pd

n = 100
rng = np.random.RandomState(1993)
x = 0.2 * rng.rand(n)
y = 31*x + 2.1 + rng.randn(n)

df = pd.DataFrame({'x': x, 'y': y})

import altair as alt

(alt.Chart(df, background='white')
    .mark_circle(color='red', size=50)
    .encode(
        x='x',
        y='y'
    )
)

from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(df[['x']], df['y'])
model.coef_
model.intercept_

# classification problem

from sklearn.datasets import make_classification

X, y = make_classification(
    n_samples=100,
    n_features=3,
    n_redundant=1,
    n_repeated=0,
    n_informative=2,
    n_classes=2,
    n_clusters_per_class=2,
    flip_y=0.05,
    class_sep=0.90,
    shuffle=True,
    random_state=1993
)

df = pd.DataFrame(X)
df['y'] = y


(alt.Chart(df)
    .mark_circle().encode(
        x=alt.X(alt.repeat('column'), type='quantitative'),
        y=alt.Y(alt.repeat('row'), type='quantitative'),
        color='y:N')
    .properties(
        width=100,
        height=100)
    .repeat(
        background='white',
        row=['0', '1', '2'],
        column=['0', '1', '2'])
    .interactive()
)
