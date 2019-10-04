import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import random

%matplotlib inline

def create_data():
    N = 1000
    x1 = np.random.normal(loc=0, scale=1, size=N)
    x2 = np.random.normal(loc=0, scale=1, size=N)
    x3 = np.random.randint(2, size=N) + 1
    # linear combination
    z = 1 + 2*x1 + -3*x2 + 0.5*x3
    # inv-logit function
    pr = [1 / (1 + np.exp(-i)) for i in z]
    y = np.random.binomial(1, p=pr, size=N)
    return y, x1, x2, x3

np.random.seed(1993)
y, x1, x2, x3 = create_data()

df = pd.DataFrame({
    'y':y,
    'x1':x1,
    'x2':x2,
    'x3':x3
})

df.head(5)

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
# from sklearn.utils import resample

X = df[['x1', 'x2', 'x3']]
y = df['y']
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=0)

model = LogisticRegression(fit_intercept=False)
model.fit(X_train, y_train)

from sklearn.metrics import accuracy_score, roc_auc_score
predicted = model.predict(X_test)
probs = model.predict_proba(X_test)

print("Accuracy:", accuracy_score(y_test, predicted))
print("AUC:", roc_auc_score(y_test, probs[:, 1]))

from sklearn.metrics import classification_report, confusion_matrix
expected = y_test
predicted = model.predict(X_test)

print(classification_report(expected, predicted))
# print(confusion_matrix(expected, predicted))

# roc curves
from sklearn.metrics import roc_curve, auc
y_score = model.fit(X_train, y_train).decision_function(X_test)
fpr, tpr, _ = roc_curve(y_test, y_score)
roc_auc = auc(fpr, tpr)

plt.figure()
lw = 2
plt.plot(fpr, tpr, color='orange', lw=lw, label='AUC: {}'.format(roc_auc))
plt.plot([0, 1], [0, 1], color='blue', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend(loc="lower right")
plt.show();

#############
# GOODREADS #
#############

df = pd.read_csv("goodreads_library_export.csv")
df = df[['Title', 'Author', 'My Rating', 'Average Rating', 'Number of Pages', 'Year Published', 'Date Read', 'Date Added', 'Bookshelves']]
df = df.dropna(axis=0, how='any')
df['Textbook'] = df['Bookshelves'].str.contains('textbook').astype('int64')
df['Date Read'] = pd.to_datetime(df['Date Read'])
df['Date Added'] = pd.to_datetime(df['Date Added'])
df['Days'] = (df['Date Read'] - df['Date Added']).dt.days
df['Days'] = np.where(df['Days']<=0, 1, df['Days'])
df['Pages Per Day'] = df['Number of Pages'] / df['Days']
df['Liked'] = np.where(df['My Rating']>=4, 1, 0)
df = df[['Liked', 'Average Rating', 'Textbook', 'Pages Per Day', 'Year Published']]
df.to_csv("df.csv", index=False)

df = pd.read_csv("df.csv")
df.head(10)

# Model 1 (garbage)

X = df[['Textbook', 'Pages Per Day', 'Year Published']]
y = df['Liked']
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=0)

import time
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB

dict_classifiers = {
    "Logistic Regression": LogisticRegression(),
    "Nearest Neighbors": KNeighborsClassifier(),
    "Linear SVM": SVC(),
    "Gradient Boosting Classifier": GradientBoostingClassifier(),
    "Decision Tree": tree.DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier(n_estimators = 18),
    "Neural Net": MLPClassifier(alpha = 1),
    "Naive Bayes": GaussianNB()
}

no_classifiers = len(dict_classifiers.keys())

def batch_classify(X_train, Y_train, X_test, Y_test, verbose = True):
    df_results = pd.DataFrame(
        data=np.zeros(shape=(no_classifiers,4)),
        columns = ['classifier', 'train_score', 'test_score', 'training_time'])
    count = 0
    for key, classifier in dict_classifiers.items():
        t_start = time.clock()
        classifier.fit(X_train, Y_train)
        t_end = time.clock()
        t_diff = t_end - t_start
        train_score = classifier.score(X_train, Y_train)
        test_score = classifier.score(X_test, Y_test)
        df_results.loc[count,'classifier'] = key
        df_results.loc[count,'train_score'] = train_score
        df_results.loc[count,'test_score'] = test_score
        df_results.loc[count,'training_time'] = t_diff
        if verbose:
            print("trained {c} in {f:.2f} s".format(c=key, f=t_diff))
        count+=1
    return df_results

df_results = batch_classify(X_train, y_train, X_test, y_test)
display(df_results.sort_values(by='test_score', ascending=False))

from sklearn.ensemble import GradientBoostingClassifier
model = GradientBoostingClassifier()
model.fit(X_train, y_train)

from sklearn.metrics import roc_curve, auc

probs = model.predict_proba(X_test)
preds = probs[:,1]
fpr, tpr, threshold = metrics.roc_curve(y_test, preds)
roc_auc = metrics.auc(fpr, tpr)

plt.plot(fpr, tpr, 'b', label = 'AUC = {}'.format(roc_auc))
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.title('ROC Curve')
plt.show();

# separation plots

def separation_plot(y_true, y_pred):
    # prepare data
    sp = pd.DataFrame({'y_true': y_true, 'y_pred': y_pred})
    sp.sort_values('y_pred', inplace=True)
    sp.reset_index(level=0, inplace=True)
    sp['index'] = sp.index
    sp['height'] = 1
    sp['y_true'] = sp.y_true.astype(np.int64)
    sp['color'] = ['b' if i == 0 else 'r' for i in sp['y_true']]
    # plot data
    plt.rcParams["figure.figsize"] = (12, 4)
    plt.bar(sp['index'], sp['height'], color=sp['color'],
        alpha = 0.75, width = 1.01, antialiased=True)
    plt.plot(sp['index'], sp['y_pred'], c='black')
    # plt.scatter(sp['y_pred'].sum(), 0.01, c='black', s=100, marker="^")
    plt.xticks([])
    plt.yticks([0, 0.5, 1])
    plt.ylabel('Predicted Value')
    plt.show()

y_true = y_test
y_pred = model.predict_proba(X_test)[:, 1]
separation_plot(y_true, y_pred)

# better model

X = df[['Average Rating', 'Pages Per Day']]
y = df['Liked']
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=0)

df_results = batch_classify(X_train, y_train, X_test, y_test)
display(df_results.sort_values(by='test_score', ascending=False))

from sklearn import tree
model = tree.DecisionTreeClassifier()
model.fit(X_train, y_train)

from sklearn.metrics import roc_curve, auc

probs = model.predict_proba(X_test)
preds = probs[:,1]
fpr, tpr, threshold = metrics.roc_curve(y_test, preds)
roc_auc = metrics.auc(fpr, tpr)

plt.title('ROC Curve')
plt.plot(fpr, tpr, 'b', label = 'AUC = {}'.format(roc_auc))
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show();

y_true = y_test
y_pred = model.predict_proba(X_test)[:, 1]
separation_plot(y_true, y_pred)


#
