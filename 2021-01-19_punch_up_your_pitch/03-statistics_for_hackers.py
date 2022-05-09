import numpy as np

# problem 1 - coins

def coin():
    return np.random.choice([1, 0])

results = [coin() for _ in range(100)]
sum(results) / 100

N = 10_000
M = 0
for _ in range(N):
    trials = np.random.randint(2, size=30)
    if (trials.sum() >= 22):
        M += 1
p = M / N
print(p)

# problem 2 - yertle

turtles = np.array([
    48, 24, 32, 61, 51, 12, 32, 18, 19, 24,
    21, 41, 29, 21, 25, 23, 42, 18, 23, 13
])

N = 10_000

xbars = np.zeros(N)
for i in range(N):
    sample = np.random.choice(turtles, size=20)
    xbars[i] = sample.mean()

xbars.mean(), xbars.std()



#
