import pandas as pd
from sklearn.model_selection import train_test_split
import tensorflow as tf
from sklearn.metrics import r2_score
import coremltools as ct

# load
df = pd.read_csv('data/games.csv')

# split
target = 'rating'
predictors = [
    'time', 'age', 'complexity', 'abstract',
    'childrens', 'customizable', 'family', 'party',
    'strategy', 'thematic', 'wargames'
]
y = df[target]
X = df[predictors]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

# create
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(8, activation=tf.nn.relu),
    tf.keras.layers.Dense(4, activation=tf.nn.relu),
    tf.keras.layers.Dense(1),
])

# compile
model.compile(
    optimizer=tf.keras.optimizers.RMSprop(),
    loss=tf.keras.losses.mean_squared_error,
    metrics=tf.keras.metrics.mean_absolute_error
)

# train
model.fit(X_train, y_train, epochs=500, batch_size=32, validation_data=(X_test, y_test))

# evaluate
r2_score(y_test, model.predict(X_test).flatten())

# convert
coreml_model = ct.convert(model)
coreml_model.save('models/BoardGameRegressor2.mlmodel')
