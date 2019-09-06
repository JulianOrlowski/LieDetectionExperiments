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

features = pd.read_csv(sys.argv[2])
labels=np.array(features['mind_condition'])
features=features.drop('mind_condition', axis=1)
feature_list = list(features.columns)
features=np.array(features)

train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.25, random_state=42)

#print('Training Features Shape:', train_features.shape)
#print('Training Labels Shape:', train_labels.shape)
#print('Testing Features Shape:', test_features.shape)
#print('Testing Labels Shape:', test_labels.shape)

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
    clf.fit(train_features, train_labels)

    predictions= clf.predict(test_features)
    print(sys.argv[1] +" :")
    print("Accuracy : " + str(accuracy_score(test_labels, predictions)) + "%.")
    print("Table of predictions: " + str(predictions))
