from IPython.display import Image, HTML

states = ['Sunny', 'Rainy', 'Snowy']

transition_matrix = [
    [0.8, 0.19, 0.01],
    [0.2,  0.7,  0.1],
    [0.1,  0.2,  0.7]
]

Image('images/helpful.jpeg', width=400)

states = [
    'Sunny', 'Sunny', 'Rainy', 'Sunny', 'Snowy',
    'Rainy', 'Rainy', 'Rainy', 'Snowy', 'Sunny',
    'Snowy', 'Snowy', 'Rainy', 'Sunny', 'Sunny',
    'Sunny', 'Sunny', 'Rainy', 'Sunny', 'Sunny'
]

Image('images/rps.jpeg', width=600)

states = ['Rock', 'Paper', 'Scissors']

transition_matrix = [
    [0.8, 0.19, 0.01],
    [0.2,  0.7,  0.1],
    [0.1,  0.2,  0.7]
]

states = [
    'Rock', 'Rock', 'Paper', 'Rock', 'Scissors',
    'Paper', 'Paper', 'Paper', 'Scissors', 'Rock',
    'Scissors', 'Scissors', 'Paper', 'Rock', 'Rock',
    'Rock', 'Rock', 'Paper', 'Rock', 'Rock'
]

HTML('<h3>"how to create a transition matrix"</h3>')

HTML('<a href="https://stackoverflow.com/a/47298184/3731467">Source</a>')

Image('images/run.jpg', width=600)

import pandas as pd

from itertools import islice

def window(seq, n=2):
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result

pairs = pd.DataFrame(window(states), columns=['state1', 'state2'])

counts = pairs.groupby('state1')['state2'].value_counts()

probs = (counts / counts.sum()).unstack()

print(probs)

Image('images/back.gif', width=400)

window(states)

list(window(states))[:5]

Image('images/light.gif', width=600)

list(zip(states, states[1:]))

Image('images/forward.gif', width=400)

print(counts)

from collections import Counter

state_to_state = list(zip(states, states[1:]))

counts = Counter(state_to_state)

counts

Image('images/panda.jpeg', width=400)

df = pd.DataFrame()
for (x, y), count in counts.items():
    df.loc[x, y] = count

print(df)
