import pandas as pd
import altair as alt

df = pd.read_csv('data/beer.csv')
df['time'] = pd.to_timedelta(df['time'] + ':00')

df = pd.melt(df,
    id_vars=['time', 'beer', 'ml', 'abv'],
    value_vars=['Mark', 'Max', 'Adam'],
    var_name='name', value_name='quantity'
)

weight = pd.DataFrame({
    'name': ['Max', 'Mark', 'Adam'],
    'weight': [165, 155, 200]
})

df = pd.merge(df, weight, how='left', on='name')

# standard drink has 17.2 ml of alcohol
df['standard_drink'] = (df['ml'] * (df['abv'] / 100) * df['quantity']) / 17.2
df['cumsum_drinks'] = df.groupby(['name'])['standard_drink'].apply(lambda x: x.cumsum())
df['hours'] = df['time'] - df['time'].min()
df['hours'] = df['hours'].apply(lambda x: x.seconds / 3600)

def ebac(standard_drinks, weight, hours):
    # https://en.wikipedia.org/wiki/Blood_alcohol_content
    BLOOD_BODY_WATER_CONSTANT = 0.806
    SWEDISH_STANDARD = 1.2
    BODY_WATER = 0.58
    META_CONSTANT = 0.015

    def lb_to_kg(weight):
        return weight * 0.4535924

    n = BLOOD_BODY_WATER_CONSTANT * standard_drinks * SWEDISH_STANDARD
    d = BODY_WATER * lb_to_kg(weight)

    bac = (n / d - META_CONSTANT * hours)
    return bac

df['bac'] = df.apply(
    lambda row: ebac(
        row['cumsum_drinks'], row['weight'], row['hours']
    ), axis=1
)

mh = df[df['name'] == 'Max'][['time', 'bac']]

# def timedelta_to_datetime(date, timedelta):
#     t = timedelta.to_pytimedelta()
#     d = pd.Timestamp(date)
#     return (d + t).to_pydatetime()
#
# mh['datetime'] = mh.apply(lambda row: timedelta_to_datetime('2018-04-21', row['time']), axis=1)

ratings = pd.read_csv('data/ratings.csv')

ratings = pd.melt(ratings,
    id_vars=['beer'],
    value_vars=['Mark', 'Max', 'Adam'],
    var_name='name', value_name='rating'
)

df = pd.merge(df, ratings, how='left', on=['name', 'beer'])


(alt.Chart(
        df[['rating', 'bac', 'name']],
        background='white',
        title='12 Beers'
    )
    .mark_circle(opacity=0.9, size=80)
    .encode(x='bac', y='rating', color='name')
    .properties(height=400, width=600)
    .interactive()
)
