from IPython.display import Image
from unittest import mock
from collections import Counter
import numpy as np

self = mock.Mock()

self.states = ['Rock', 'Paper', 'Scissors']

self.index_dict = {self.states[index]: index for index in
    range(len(self.states))}

self.state_dict = {index: self.states[index] for index in
    range(len(self.states))}

Image('images/tools.jpg', width=400)

from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()

states = [
    'Rock', 'Rock', 'Paper', 'Rock', 'Scissors',
    'Paper', 'Paper', 'Paper', 'Scissors', 'Rock',
    'Scissors', 'Scissors', 'Paper', 'Rock', 'Rock',
    'Rock', 'Rock', 'Paper', 'Rock', 'Rock'
]

le.fit(states)

chain = le.fit_transform(states)

print(chain)

le.inverse_transform(chain)

state_to_state = list(zip(chain, chain[1:]))

counts = Counter(state_to_state)

unique = len(set(chain))

matrix = [[0 for _ in range(unique)] for _ in range(unique)]

for (x, y), count in counts.items():
    matrix[x][y] = count

print(matrix)

Image('images/wrap.gif', width=600)

def chain_to_matrix(chain):
    counts = Counter(zip(chain, chain[1:]))
    unique = len(set(chain))
    matrix = [[0 for _ in range(unique)] for _ in range(unique)]
    for (x, y), count in counts.items():
        matrix[x][y] = count
    return matrix

matrix = chain_to_matrix(chain)

print(matrix)

Image('images/normal.png', width=600)

def normalize(x):
    x_sum = sum(x)
    return [i / x_sum for i in x]

normalize([5, 3, 2])

normalize([12, 22, 11])

Image('images/iterate.png', width=600)

def normalize_matrix(matrix):
    normalized_matrix = []
    for row in matrix:
        normalized_row = normalize(row)
        normalized_matrix.append(normalized_row)
    return normalized_matrix

transition_matrix = normalize_matrix(matrix)

print(transition_matrix)

Image('images/run.jpg', width=600)

# def next_state(self, current_state):
#     return np.random.choice(
#         self.states,
#         p=self.transition_matrix[self.index_dict[current_state], :]
#     )

def next_state(current_state):
    return np.random.choice(
        le.classes_,
        p=transition_matrix[le.transform([current_state])[0]]
    )

next_state('Rock')

Image('images/thor.gif', width=600)
