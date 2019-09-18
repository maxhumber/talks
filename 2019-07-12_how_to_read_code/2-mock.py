from IPython.display import Image
import numpy as np

Image('images/minimal.png', width=600)

states = ['Sunny', 'Rainy', 'Snowy']

transition_matrix = [
    [0.8, 0.19, 0.01],
    [0.2,  0.7,  0.1],
    [0.1,  0.2,  0.7]
]

Image('images/head.gif', width=600)

# class MarkovChain(object):
# def __init__(self, transition_matrix, states):

from unittest import mock
self = mock.Mock()

Image('images/usual.jpg', width=600)

self.transition_matrix = np.atleast_2d(transition_matrix)
self.states = states
self.index_dict = {self.states[index]: index for index in
    range(len(self.states))}
self.state_dict = {index: self.states[index] for index in
    range(len(self.states))}

def next_state(self, current_state):
    return np.random.choice(
        self.states,
        p=self.transition_matrix[self.index_dict[current_state], :]
    )

def generate_states(self, current_state, no=10):
    future_states = []
    for i in range(no):
        next_state = self.next_state(current_state)
        future_states.append(next_state)
        current_state = next_state
    return future_states
