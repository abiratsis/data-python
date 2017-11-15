import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

cancer = load_breast_cancer()

cancer_data = np.c_[cancer['data'], cancer['target']] 
cancer_cols = np.append(cancer.feature_names, ['target'])

df = pd.DataFrame(data = cancer_data, columns = cancer_cols)

distribution = len(df[df['target'] == 0]),  len(df[df['target'] == 1])

s = pd.Series(data=distribution, index=['malignant','benign'], name='target')

y = df['target']
X = df.drop('target', axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

knn = KNeighborsClassifier(n_neighbors = 1)
knn.fit(X_train, y_train)
means = df.mean()[:-1].values.reshape(1, -1)
res = knn.predict(means)

res