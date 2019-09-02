import pandas as pd
import numpy as np
import math
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn import metrics

features = pd.read_csv('testall_test_filter7.csv')
print(features.head(5))

labels=np.array(features['mind_condition'])
features=features.drop('mind_condition', axis=1)
feature_list = list(features.columns)
features=np.array(features)

train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.25, random_state=42)

print('Training Features Shape:', train_features.shape)
print('Training Labels Shape:', train_labels.shape)
print('Testing Features Shape:', test_features.shape)
print('Testing Labels Shape:', test_labels.shape)

#RandomForest
rf = RandomForestRegressor(n_estimators=1000, random_state=42)
rf.fit(train_features, train_labels)
predictions = rf.predict(test_features)


#SVM
clf = svm.SVC(gamma='scale')
clf.fit(train_features, train_labels)

predictions_svm = clf.predict(test_features)

good_prediction=0
good_prediction_svm=0

for i in range(len(predictions)):
    if (predictions[i]%1) < 0.5:
        predictions[i] = math.floor(predictions[i])
    else:
        predictions[i] = math.ceil(predictions[i])
    if (predictions_svm[i]%1) < 0.5:
        predictions_svm[i] = math.floor(predictions_svm[i])
    else:
        predictions_svm[i] = math.ceil(predictions_svm[i])
    if predictions[i] == test_labels[i]:
        good_prediction+=1
    if predictions_svm[i] == test_labels[i]:
        good_prediction_svm+=1

print('Accuracy of RandomForest: ', (100*(good_prediction))/len(predictions), '%.')
print('Accuracy of SVM: ', (100*(good_prediction_svm))/len(predictions_svm), '%.')

#Logistic
logreg = LogisticRegression()
logreg.fit(train_features, train_labels)
y_pred = logreg.predict(test_features)
print('Accuracy of logistic regression classifier on test set:{:.2f}'.format(logreg.score(test_features, test_labels)))
