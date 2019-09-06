#!/usr/bin/env python3

import pandas as pd
import numpy as np
import json
import ast
import apsw
import math
import sys
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn import metrics
from sklearn.metrics import make_scorer, accuracy_score
from sklearn.model_selection import GridSearchCV

data_train = pd.read_csv(sys.argv[2])
data_test = pd.read_csv(sys.argv[3])

X_all=data_train.drop(['mind_condition'], axis=1)
y_all=data_train['mind_condition']

num_test=0.20
X_train, X_test, y_train, y_test=train_test_split(X_all, y_all, test_size=num_test, random_state=23)

clf1=RandomForestClassifier()
clf2=svm.SVC(gamma='scale')
clf3=LogisticRegression(solver='lbfgs', multi_class='multinomial', random_state=1)

if sys.argv[1]=="RandomForest":
    clf=clf1
elif sys.argv[1]=="SVM":
    clf=clf2
elif sys.argv[1]=="Logistic":
    clf=clf3
else:
    clf = None

if clf is not None:
    clf.fit(X_train, y_train)

    predictions= clf.predict(X_test)
    #predictions = clf1.predict(data_test.drop('mind_condition', axis=1))
    print(sys.argv[1] +" :")
    print("Accuracy : " + str(accuracy_score(y_test, predictions)) + "%.")
    print("Table of predictions: " + str(predictions))
