from IPython.display import Image, HTML
import re
import random

HTML('<h2>https://github.com/maxhumber/marc/</h2>')

HTML('<h2>pip install marc</h2>')

from marc import MarkovChain

chain = [
    'Rock', 'Rock', 'Paper', 'Rock', 'Scissors',
    'Paper', 'Paper', 'Paper', 'Scissors', 'Rock',
    'Scissors', 'Scissors', 'Paper', 'Rock', 'Rock',
    'Rock', 'Rock', 'Paper', 'Rock', 'Rock'
]

mc = MarkovChain(chain)

mc.next_state('Rock')

mc.generate_states('Paper', n=5)

mc.next_state('Scissors')

Image('images/shakespeare.gif', width=600)

def build_chain(file):
    with open(file, 'r') as f:
        data = f.read()
    words = re.findall(r"[\w']+|[.,!?;]", data)
    chain = [word.lower() for word in words]
    return MarkovChain(chain)

def generate_sentences(mc, n=5, length=(15, 30)):
    for _ in range(n):
        l = random.randint(length[0], length[1])
        nonsense = ' '.join(mc.generate_states(n=l))
        nonsense = re.sub(r'\s+([.,!?;])', r'\1', nonsense)
        print(nonsense)
        print()

othello = build_chain('data/othello.txt')
random.seed(21)
generate_sentences(othello)

oz = build_chain('data/oz.txt')
generate_sentences(oz)
