from IPython.display import Image
import numpy as np
from unittest import mock

Image('images/pika.gif', width=600)

states = ['Sunny', 'Rainy', 'Snowy']

transition_matrix = [
    [0.8, 0.19, 0.01],
    [0.2,  0.7,  0.1],
    [0.1,  0.2,  0.7]
]

self = mock.Mock()

self.transition_matrix = np.atleast_2d(transition_matrix)

self.states = states

self.index_dict = {self.states[index]: index for index in
    range(len(self.states))}

self.state_dict = {index: self.states[index] for index in
    range(len(self.states))}

Image('images/skeptical.gif', width=400)

current_state = 'Sunny'

def next_state(self, current_state):
    return np.random.choice(
        self.states,
        p=self.transition_matrix[self.index_dict[current_state], :]
    )

next_state(self, current_state)

Image('images/deeper.jpeg', width=600)

self.transition_matrix[self.index_dict[current_state], :]

def generate_states(self, current_state, no=10):
    future_states = []
    for i in range(no):
        next_state = self.next_state(current_state)
        future_states.append(next_state)
        current_state = next_state
    return future_states

Image('images/loop.jpg', width=600)

future_states = []

i = 1
ns = next_state(self, current_state)
future_states.append(ns)
current_state = ns
