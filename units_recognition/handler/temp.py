import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
from sklearn.utils import resample
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score


# df = pd.read_csv('/home/sfelshtyn/Python/SapLabApp/resources/static/symbols_for_SVM_21_test.csv')
# X = df.iloc[: , 1:].copy()
# # X = X.astype('int32').dtypes
# y = df.iloc[:, 0].copy()
#
# X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=2, shuffle=True)
# X_train_scaled = scale(X_train)
# X_test_scaled = scale(X_test)
#
# clf_svm = SVC(random_state=42, C=10, gamma='scale', kernel='rbf')
# clf_svm.fit(X_train_scaled, y_train)
# joblib.dump(clf_svm, '/units_recognition/handler/classifier')   # /home/sfelshtyn/Python/SapLabApp/units_recognition/handler

df2 = pd.read_csv('/home/sfelshtyn/Python/SapLabApp/resources/static/symbols_for_SVM_21_test.csv')
X2 = scale(df2.iloc[: , 1:].copy())
y2 = df2.iloc[:, 0].copy()

clf_svm = joblib.load("/home/sfelshtyn/Python/SapLabApp/units_recognition/handler/classifier")
y_pred = clf_svm.predict(X2)

print(accuracy_score(y2, y_pred))
