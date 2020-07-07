#################################
##                             ##
##   I N T R O D U C T I O N   ##
##                             ##
#################################

from IPython.display import Image, IFrame, HTML

Image('https://images.newscientist.com/wp-content/uploads/2016/03/pronounce-copy.gif', width=500)

HTML('<h1><a style="color: white" href="https://github.com/maxhumber/gif">https://github.com/maxhumber/gif</a></h1>')

IFrame('https://ndres.me/post/matplotlib-animated-gifs-easily/', width=800, height=500)

#################################
##                             ##
##        E X P L O R E        ##
##                             ##
#################################

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/textbooks.csv')

df.head()

df['read'] = pd.to_datetime(df['read'])

days = (df['read'].max() - df['read'].min())

print(days)

plt.scatter(df['read'], df['pages'], s=60);

#################################
##                             ##
##           P R E P           ##
##                             ##
#################################

colors = {
    'Swift': '#fd9426',
    'R': '#5fc9f8',
    'Python': '#fecb2e'
}

df['color'] = df['language'].map(colors).fillna('#8e8e93')

date = pd.Timestamp('2017-01-10')

d = df[df['read'] <= date]

fig, ax = plt.subplots(figsize=(12, 7))
plt.scatter(d['read'], d['pages'], c=d['color'], s=60)
ax.set_xlim([date - pd.Timedelta('2000 days'), date + pd.Timedelta('1 day')])
ax.set_ylim([0, 1200])
ax.set_yticklabels([0, 200, 400, 600, 800, 1000, '\n1200\npages']);

#################################
##                             ##
##           P L O T           ##
##                             ##
#################################

def plot(date):
    x_start = date - pd.Timedelta('2000 days')
    x_end = date + pd.Timedelta('1 day')
    d = df[df['read'] <= date]
    fig, ax = plt.subplots(figsize=(12, 7))
    plt.scatter(d['read'], d['pages'], c=d['color'], s=60)
    ax.set_xlim([x_start, x_end])
    ax.set_ylim([0, 1200])
    ax.set_yticklabels([0, 200, 400, 600, 800, 1000, '\n1200\npages'])
    plt.title('Textbooks')

plot(pd.Timestamp('2018-01-01'))

#################################
##                             ##
##            G I F            ##
##                             ##
#################################

import gif # pip install gif

@gif.frame
def plot(date):
    x_start = date - pd.Timedelta('2000 days')
    x_end = date + pd.Timedelta('1 day')
    d = df[df['read'] <= date]
    fig, ax = plt.subplots(figsize=(12, 7))
    plt.scatter(d['read'], d['pages'], c=d['color'], s=60)
    ax.set_xlim([x_start, x_end])
    ax.set_ylim([0, 1200])
    ax.set_yticklabels([0, 200, 400, 600, 800, 1000, '\n1200\npages'])
    plt.title('Textbooks')

dates = pd.date_range(
    start=df['read'].min() - pd.Timedelta('50 days'),
    end=pd.Timestamp('now') + pd.Timedelta('50 days'),
    freq='4D'
)

frames = []
for date in dates:
    frame = plot(date)
    frames.append(frame)

gif.save(frames, 'output/complacency-4d.gif', duration=40)

Image('output/complacency-4d.gif', width=500)

Image('https://media.giphy.com/media/12NUbkX6p4xOO4/giphy.gif', width=500)

#################################
##                             ##
##          M O R E            ##
##                             ##
#################################

import pandas as pd
from matplotlib import pyplot as plt
import gif # pip install gif

START = pd.Timestamp('2019-04-20')
END = pd.Timestamp('2020-05-01')

data = '1.9,2.0,3.8,2.9,2.7,1.5,1.4,2.0,1.8,2.6,2.1,1.4,2.8,3.2,3.0,3.6,2.4,4.2,3.3,4.3,2.0,4.0,2.0,2.2,2.5,1.8,1.8,1.6,2.6,2.6,2.8,2.1,2.4,1.9,1.4,1.2,3.9,2.9,1.7,1.8,1.7,2.4,2.3,1.5,2.4,2.6,1.6,1.2,1.9,2.5,2.3,2.6,2.0,1.8,2.5,1.9,2.5,2.7,2.5,2.0,1.6,1.4,2.4,2.4,0.7,3.5,3.6,2.9,3.4,1.6,1.8,1.8,1.1,1.9,1.9,1.3,1.6,2.1,1.7,3.1,4.4,3.7,2.8,3.6,4.0,5.6,2.5,1.4,1.6,1.6,2.9,2.0,2.9,2.0,1.9,1.9,1.9,1.2,2.1,1.8,2.5,2.0,2.0,2.1,2.3,2.9,1.4,1.6,1.4,2.2,2.2,2.4,1.6,1.2,1.8,1.8,2.2,1.8,5.3,0.8,2.1,3.3,4.5,1.4,1.3,2.8,0.9,1.7,1.6,1.3,1.8,2.4,3.6,2.6,3.6,5.8,2.4,1.2,1.5,2.1,2.5,3.1,1.8,2.0,1.6,1.8,3.6,2.2,2.1,2.2,1.0,1.7,2.0,2.3,2.0,1.6,1.6,1.2,1.1,1.6,1.7,2.2,1.5,1.9,1.6,2.0,2.3,1.8,3.2,2.7,2.0,2.3,1.3,1.4,1.0,2.1,1.6,1.6,2.7,2.7,2.9,2.7,2.9,2.5,2.2,2.7,2.5,1.7,3.0,2.9,2.4,3.0,3.1,3.0,3.4,2.2,1.7,4.3,2.8,2.8,2.0,4.3,4.2,7.9,9.1,3.6,2.7,4.9,4.1,4.5,3.1,4.1,3.1,3.0,3.7,2.9,3.0,4.1,4.4,4.8,1.9,2.6,2.3,2.2,1.8,3.7,1.7,1.9,3.5,6.3,3.2,2.2,5.0,1.4,2.8,2.2,2.3,3.6,2.4,3.9,1.7,2.2,1.9,2.5,2.6,3.4,4.8,3.2,5.0,5.8,3.3,3.8,2.6,2.8,3.5,3.2,3.6,3.1,6.3,7.5,3.2,3.5,3.4,4.2,2.7,2.9,6.9,4.3,4.3,2.7,2.7,3.1,4.4,5.8,2.8,3.2,4.1,2.0,3.0,5.1,5.4,6.5,3.0,2.7,2.8,3.1,2.6,4.4,5.7,3.6,3.4,4.1,4.2,4.3,5.6,4.9,2.7,2.1,3.5,3.5,3.1,2.7,0.7,3.1,1.9,3.9,2.9,2.9,2.4,2.5,2.5,3.2,2.1,2.3,2.1,2.3,4.7,4.7,4.4,4.5,4.0,3.4,3.0,1.9,3.8,1.4,2.6,1.7,2.8,2.7,2.7,2.2,2.6,4.3,6.7,7.0,4.2,4.9,3.8,4.8,4.8,3.5,3.0,1.8,1.3,2.4,4.1,4.5,4.6,4.5,4.2,3.4,2.8,1.4,3.0,2.4,2.2,1.9,2.1,1.6,2.8,2.8,4.2,3.1,3.7,2.0,2.6,1.7,2.1,1.6,3.5,1.6,1.8,2.1,3.0,5.4,2.9,3.0'

df = pd.DataFrame({
    'date': pd.date_range(start=START, end=END),
    'time': [float(d) for d in data.split(',')]
})

FONT = {'fontname':'Avenir', 'fontsize': 16}
PALLET = ['#000000', '#d8e2dc']
plt.rcParams["axes.facecolor"] = PALLET[1]
plt.rcParams["figure.facecolor"] = PALLET[1]
plt.rcParams["savefig.facecolor"] = PALLET[1]

@gif.frame
def plot(date):
    d = df[df['date'] <= date]
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.plot(d['date'], d['time'], color=PALLET[0])
    ax.set_xlim([START, END])
    ax.set_ylim([0, 10])
    ax.set_xticks([date])
    ax.set_yticks([0, 2, 4, 6, 8, 10])
    ax.set_xticklabels([date.strftime("%b '%y")], **FONT)
    ax.set_yticklabels([0, 2, 4, 6, 8, '\n10\nhours'], **FONT)
    plt.title('Time on Phone', **FONT)

frames = []
for date in df['date']:
    frame = plot(date)
    frames.append(frame)

gif.save(frames, 'output/time.gif', duration=35)

Image('output/time.gif', width=500)

#################################
##                             ##
##         ☕️ C A L M          ##
##                             ##
#################################

url = 'https://calmcode.io/matplot-gif/introduction.html'

IFrame(url, width=800, height=500)

#################################
##                             ##
##        T H A N K S !        ##
##                             ##
#################################
