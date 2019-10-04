import pandas as pd
import seaborn as sns
import altair as alt

import seaborn as sns
df = sns.load_dataset('iris')

transformers = {
    'setosa': 'autobot',
    'versicolor': 'decepticon',
    'virginica': 'predacon'}

df['species'] = df['species'].map(transformers)
df.sample(10)

df.rename(
    columns={
        'sepal_length': 'leg_length',
        'sepal_width': 'leg_width',
        'petal_length': 'arm_length',
        'petal_width': 'arm_width'
    },
    inplace=True
)

(alt.Chart(df)
    .mark_circle().encode(
        x=alt.X(alt.repeat('column'), type='quantitative'),
        y=alt.Y(alt.repeat('row'), type='quantitative'),
        color='species:N')
    .properties(
        width=90,
        height=90)
    .repeat(
        background='white',
        row=['leg_length', 'leg_width', 'arm_length', 'arm_width'],
        column=['leg_length', 'leg_width', 'arm_length', 'arm_width'])
    .interactive()
)

df.to_csv('data/transformers.csv', index='False')
