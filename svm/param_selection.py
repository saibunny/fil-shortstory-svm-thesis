import numpy as np
import pandas as pd
import warnings
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier

warnings.filterwarnings("ignore")

path = "data/latest/removed_zeroes_and_duplicates_newest_consolidated_validset_wordcount6.csv"

# assign column names
colnames = ['pleasantness', 'attention', 'sensitivity', 'aptitude', 'polarity', 'emotion']

# lagay sa dataframe yung dataset
data = pd.read_csv(path, names=colnames)

# X = data.drop(data.columns[[4,5]], axis=1)
X = data.drop('emotion', axis=1)
y = data['emotion']

# train test split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)

parameter_candidates = [
    # {'estimator__C': [1, 10, 100, 1000, 10000, 100000], 'estimator__gamma': [0.1, 0.01, 0.001, 0.0001], 'estimator__kernel': ['linear']},
     # {'estimator__C': [1, 10, 100, 1000, 10000, 100000], 'estimator__gamma': [0.1, 0.01, 0.001, 0.0001], 'estimator__degree':[2,3,4,5,6,7,8],'estimator__kernel': ['poly']},
    # {'estimator__C': [1, 10, 100, 1000, 10000, 100000], 'estimator__gamma': [0.1, 0.01, 0.001, 0.0001], 'estimator__kernel': ['rbf']},
    {'estimator__C': [1, 10, 100, 1000, 10000, 100000], 'estimator__gamma': [0.1, 0.01, 0.001, 0.0001], 'estimator__kernel': ['sigmoid']}
]

ovr = OneVsRestClassifier(SVC())

clf = GridSearchCV(estimator=ovr, param_grid=parameter_candidates, n_jobs=-1)

clf.fit(X_train,y_train)

print path
print clf.best_score_
print clf.best_params_

# View accuracy score
# print('Best (accuracy) score: ', clf.best_score_)

# view best parameters for the model found using grid search
# print('Best C: ', clf.best_estimator_.estimator__C)
# print('Best Kernel: ', clf.best_estimator_.estimator__kernel)
# print('Best Gamma: ', clf.best_estimator_.estimator__gamma)