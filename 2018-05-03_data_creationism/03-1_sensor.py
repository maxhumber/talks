import pandas as pd
from traces import TimeSeries as TTS
import altair as alt
from datetime import datetime

df = pd.read_csv('data/in_and_out.csv')

(alt.Chart(
        df,
        background='white',
        title='Sensor'
    )
    .mark_circle(
        color='red',
        opacity=0.5,
        size=80
    )
    .encode(
        x='datetime:T',
        y=alt.Y('door', scale=alt.Scale(domain=(-1, 2)))
    )
    .properties(
        height=300,
        width=600
    )
    .interactive()
)

from traces import TimeSeries as TTS
from datetime import datetime

d = {}
for i, row in df.iterrows():
    date = pd.Timestamp(row['datetime']).to_pydatetime()
    door = row['door']
    d[date] = door

tts = TTS(d)

tts[datetime(2018, 4, 9)]

tts[datetime(2018, 4, 17, 8)]

tts[datetime(2018, 4, 17, 8, 59)]

tts.distribution(
    start=datetime(2018, 4,  1),
    end=datetime(2018, 4, 21)
)
