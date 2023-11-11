from sklearn import preprocessing as pp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.sparse import data
import seaborn as sns

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import datetime as dt

import warnings
warnings.filterwarnings("ignore")

dataset_path = "air-quality-dataset/_DISTRICT/"

# Loading dataset using pandas
Data = pd.read_csv(dataset_path + "q1" + ".csv")

# Tien xu ly du lieu
num = Data._get_numeric_data()
num[num < 0] = 0

# Kiem tra (checking) va dem so luong (counting) du lieu mat mat (missing data) cho moi cot (column)
Data.isnull().sum()

# Xoa gia tri mat mat (Deleting missing values)
DataCleaned = Data.dropna()
DataCleaned.isnull().sum()  # kiem tra lai lan nua


# PREDICTION
# format datetime Data
Data['date'] = pd.to_datetime(Data['date'],
                              format='%Y-%m-%d',
                              errors='coerce')

# Normalization: Chuan hoa du lieu => [0,1]
print('Min max scaling')
mms = pp.MinMaxScaler()
no2 = np.array(Data['no2'])
no2 = mms.fit_transform(no2.reshape(-1, 1))
print("====> mms", no2, "\nmin: ", no2.min(),
      "\nmean: ", no2.mean(), "\nmax: ", no2.max(),)

# feature
feature = Data
feature["no2"] = no2
feature["year"] = feature["date"].dt.year
feature["month"] = feature["date"].dt.month
#feature["week"] = feature["date"].dt.week
feature["day"] = feature["date"].dt.day
feature["no"] = feature["date"].dt.day
#feature["dayofweek"] = feature["date"].dt.dayofweek
feature = feature.drop("date", axis=1)
feature = feature.drop("dist", axis=1)
feature = feature.drop("co", axis=1)
feature = feature.drop("no2", axis=1)
feature = feature.drop("o3", axis=1)
feature = feature.drop("so2", axis=1)
feature = feature.drop("ch4", axis=1)
feature = feature.drop("hcho", axis=1)

feature.head()

# labels
label = no2
# label.head()

# test and train split
X_train, X_test, y_train, y_test = train_test_split(
    feature, label, test_size=0.05)
print("=====X_train y_train:\n", X_train.shape, y_train.shape)
print("=====X_test y_test:\n", X_test.shape, y_test.shape)

model = LinearRegression()

model.fit(X_train, y_train)

model.score(X_test, y_test)

y_pred = model.predict(X_test)

# The coefficients: Cac he so hoi quy
print("=====Cofficients: cac he so hoi quy \n", model.coef_)

# The mean square error: Loi binh phuong trung binh
print("=====Mean square error: %.2f" % mean_squared_error(y_test, y_pred))

# The coefficient of determination: 1 is perfect prediction: 1 is perfect prediction
print("=====Coefficient of dtermination: %.2f" % r2_score(y_test, y_pred))

# The R squared value
print("=====R squared value: %.2f" % r2_score(y_test, y_pred))

plt.plot(range(y_test.shape[0]), y_test, 'r.', label="true")
plt.plot(range(y_test.shape[0]), y_pred, 'g.', label="prediction")
plt.legend(loc="best")

print(1111)
