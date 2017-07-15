# regulators

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.interpolate import splrep, splev

%matplotlib inline
plt.rcParams["figure.figsize"] = (12, 9)

table = [
    ['prob', 'deductible'],
    [0.20, 5000],
    [0.18, 4800],
    [0.17, 4600],
    [0.10, 2400],
    [0.05, 1300],
    [0.04, 1200],
    [0.02, 1000]
]
headers = table.pop(0)

df = pd.DataFrame(table, columns=headers)
df
X = np.arange(0, 0.5, 0.01)

plt.plot(df['prob'], df['deductible'], linewidth=2, label='Current') # 1
plt.plot(X, X*25000 + -1000, 'r', label='Model') # 2
plt.ylim(0, 6000)
plt.xlim(0, 0.25)
plt.xlabel('Accident Risk')
plt.ylabel('Deductible')
plt.legend()
plt.title('Deductible Curves', loc='left')
plt.grid(True)
plt.show();

def curve(x, ymin, ymax, xhl, xhu, up=True):
    a = (xhl + xhu) / 2
    b = 2 / abs(xhl - xhu)
    c = ymin
    d = ymax - c
    if up == True:
        y = c + ( d / ( 1 + np.exp(1)**( -b * (x - a) ) ) )
    elif up == False:
        y = c + ( d / ( 1 + np.exp( b * (x - a) ) ) )
    else:
        None
    return y

v = curve(0.05, ymin=1000, ymax=5000, xhl=0.12, xhu=0.18)
print(v)

curve_example = pd.DataFrame({'x': np.arange(0, 100, 1)})
curve_example = curve_example.assign(y1 = curve(curve_example.x, ymin=30, ymax=80, xhl=40, xhu=60))
curve_example = curve_example.assign(y2 = curve(curve_example.x, ymin=10, ymax=50, xhl=10, xhu=50))
curve_example = curve_example.assign(y3 = curve(curve_example.x, ymin=40, ymax=90, xhl=50, xhu=60, up=False))

plt.plot(curve_example['x'], curve_example['y1'], linewidth=2, label='curve(30, 80, 40, 60)') # 1
plt.plot(curve_example['x'], curve_example['y2'], linewidth=2, label='curve(10, 50, 10, 50)') # 2
plt.plot(curve_example['x'], curve_example['y3'], linewidth=2, label='curve(40, 90, 50, 60, down)') # 3
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.title('Curve Function Example', loc="left")
plt.legend(loc=4)
plt.grid(True)
plt.show();

df_new = pd.DataFrame({'prob': np.arange(0, 0.30, 0.005)})
df_new = df_new.assign(deductible=curve(df_new.prob, ymin=1000, ymax=5000, xhl=0.12, xhu=0.18))

plt.plot(df['prob'], df['deductible'], linewidth=2, label='Current', ls='dashed')
plt.plot(X, X*25000 + -1000, c='red', label='Model', ls='dotted')
plt.plot(df_new['prob'], df_new['deductible'], c='orange', linewidth=4, label="Proposed")
plt.ylim(0, 6000)
plt.xlim(0, 0.25)
plt.title('Deductible Curve', loc="left")
plt.ylabel('Deductible')
plt.xlabel('Accident Risk')
plt.grid(True)
plt.legend(loc=4)
plt.show();

# infrastructure

import numpy as np
import pandas as pd
from itertools import product
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
from matplotlib import pyplot as plt

%matplotlib inline
plt.rcParams["figure.figsize"] = (12, 9)

# FAKE DATA

features, output = make_classification(
    n_samples = 1000,
    n_features = 3,
    n_informative = 3,
    n_redundant = 0,
    n_classes = 2,
    flip_y = 0.05,
    shift = [0, 0, 0],
    weights = [.4, .6],
    random_state = 1993)

colors = ['red' if i == 1 else 'blue' for i in output]
colors

f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)
ax1.scatter(features[:,0], features[:,1], c=colors, alpha=0.5)
ax2.scatter(features[:,1], features[:,2], c=colors, alpha=0.5)
ax3.scatter(features[:,0], features[:,2], c=colors, alpha=0.5)

df = pd.DataFrame(features, output)
df.columns = ['x1', 'x2', 'x3']
df['y'] = df.index
df.head(20)

output = to_categorical(output)
ncols = features.shape[1]

X_train, X_test, y_train, y_test = train_test_split(features, output, train_size=0.8, random_state=42)

# KERAS

from keras.models import Sequential
from keras.layers import Dense

model = Sequential()
model.add(Dense(16, activation='relu', input_shape=(ncols,)))
model.add(Dense(2, activation='softmax')) # to sum to 1
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=["accuracy"])
model.fit(X_train, y_train, epochs=10, batch_size=1, verbose=1);

loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy = {:.2f}".format(accuracy))

new_data = np.array([[-2, -2, 0.7]])

model.predict_classes(new_data)
model.predict(new_data)
model.predict(new_data)[0][1]

# EXPAND GRID

combos = {
    'x1': np.arange(-2, 2, 0.1),
    'x2': np.arange(-2, 2, 0.1),
    'x3': np.arange(-2, 2, 0.1)
}

def expand_grid(data_dict):
    """Create a dataframe from every combination of given values."""
    rows = product(*data_dict.values())
    return pd.DataFrame.from_records(rows, columns=data_dict.keys())

crystal = expand_grid(combos)
crystal = crystal.apply(lambda df: np.round(df, decimals=1))
crystal.head(10)

crystal_in = np.array(crystal.values.tolist())
crystal_pred = pd.DataFrame(model.predict(crystal_in))

df_c = pd.concat([crystal.reset_index(drop=True), crystal_pred], axis=1)
df_c[4000:4005]
df_c[39000:39005]
df_c[50000:50005]
