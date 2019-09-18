import datetime
from dateutil import rrule
from recurrent import RecurringEvent #pip install recurrent
import pandas as pd
import yaml #pip install pyyaml
import fire #pip install fire
import altair as alt

start = pd.Timestamp('today').normalize()
end = start + datetime.timedelta(days=365)

def get_dates(frequency):
    try:
        return [pd.Timestamp(frequency).normalize()]
    except ValueError:
        pass
    try:
        r = RecurringEvent()
        r.parse(frequency)
        rr = rrule.rrulestr(r.get_RFC_rrule())
        return [pd.to_datetime(date).normalize() for date in rr.between(start, end)]
    except ValueError:
        raise ValueError('Invalid frequency')

def run(file):
    print('Working...')
    with open(file, 'r') as f:
        budget = yaml.load(f)
    calendar = pd.DataFrame(index=pd.date_range(start=start, end=end))
    for k, v in budget.items():
        frequency = v.get('frequency')
        amount = v.get('amount')
        dates = get_dates(frequency)
        i = pd.DataFrame(
            data={k: amount},
            index=pd.DatetimeIndex(pd.Series(dates))
        )
        calendar = pd.concat([calendar, i], axis=1).fillna(0)
    calendar['balance'] = calendar.sum(axis=1).cumsum()
    return calendar

def plot(file='budget.yaml', output=f'budget_{start.date()}.png'):
    calendar = run(file)
    vis = (
        alt.Chart(calendar.reset_index())
        .mark_line(color='red')
        .encode(
            x=alt.X('index', title=''),
            y=alt.Y('balance', title='Balance'),
            tooltip='balance'
        )
        .interactive()
        .properties(width=900, height=600, title='Forecast', background='white')
    )
    vis.save(output)
    print('Success!')

def csv(file='budget.yaml', output=f'budget_{start.date()}.csv'):
    calendar = run(file)
    calendar.to_csv(output, index=True)
    print('Success!')
