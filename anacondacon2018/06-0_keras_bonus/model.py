import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from sklearn_pandas import DataFrameMapper, CategoricalImputer
from helpers import DateEncoder
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier

df = pd.read_csv('../max_bike_data.csv')
df['time'] = pd.to_datetime(df['time'])
df = df[(df['pick_up'].notnull()) & (df['drop_off'].notnull())]

TARGET = 'drop_off'
y = df[TARGET].values
X = df.drop(TARGET, axis=1)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

lb = LabelBinarizer()
y_train = lb.fit_transform(y_train)

# need to transform the x variables
mapper = DataFrameMapper([
    ('time', DateEncoder(), {'input_df': True}),
    ('pick_up', LabelBinarizer()),
    ('last_drop_off', [CategoricalImputer(), LabelBinarizer()]),
    ('last_pick_up', [CategoricalImputer(), LabelBinarizer()])
])

X_train_m = mapper.fit_transform(X_train)

def model():
    model = Sequential()
    model.add(Dense(24, activation='relu', input_dim=X_train_m.shape[1]))
    model.add(Dense(12, activation='relu'))
    model.add(Dense(y_train.shape[1], activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


kc = KerasClassifier(build_fn=model, epochs=200, batch_size=1, verbose=2)
kc.fit(X_train_m, y_train)

X_test_m = mapper.transform(X_test)
y_test = lb.transform(y_test)
lb.inverse_transform(y_test)


kc.predict(X_test_m)
kc.predict_proba(X_test_m)
kc.score(X_test_m, y_test)

y_test_pred = kc.predict_proba(X_test_m)
y_test_pred = (y_test_pred == y_test_pred.max(axis=1, keepdims=1)).astype(float)
lb.inverse_transform(y_test_pred)
lb.inverse_transform(y_test)


pd.DataFrame({
    'real': lb.inverse_transform(y_test),
    'pred': lb.inverse_transform(y_test_pred)
})


#
