import pandas as pd
import numpy as np
import seaborn as sns

df = sns.load_dataset('titanic')
df = df[['survived', 'pclass', 'sex', 'age', 'fare']].copy()
df

df.rename(
    columns={
        'survived': 'mummified',
        'pclass': 'class',
        'fare': 'debens'
    }, inplace=True)

df['debens'] = round(df['debens'] * 10, -1)

# inverse
df['mummified'] = np.where(df['mummified'] == 0, 1, 0)

df = pd.get_dummies(df)
df = df.drop('sex_female', axis=1)
df.rename(columns={'sex_male': 'male'}, inplace=True)

df

df.to_csv('data/mummy.csv', index=False)
