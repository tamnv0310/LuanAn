#dataset: hcm-3
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

dataset_path = "air-quality-dataset/_DISTRICT-ALL/"

#limits from sentinel 5p: https://docs.sentinel-hub.com/api/latest/data/sentinel-5p-l2/
limits = {
    "co": {"min": 0, "max": 0.1},
    "hcho": {"min": 0, "max": 0.001},
    "no2": {"min": 0, "max": 0.0003},
    "o3": {"min": 0, "max": 0.36},
    "so2": {"min": 0, "max": 0.01},
    "ch4": {"min": 1600, "max": 2000},
}

# Loading dataset using pandas
Data = pd.read_csv(dataset_path + "hcm-3" + ".csv")

#Tien xu ly du lieu
num = Data._get_numeric_data()
num[num < 0] = 0

# Kiem tra (checking) va dem so luong (counting) du lieu mat mat (missing data) cho moi cot (column)
Data.isnull().sum()

# Xoa gia tri mat mat (Deleting missing values)
DataCleaned = Data.dropna()
DataCleaned.isnull().sum()  # kiem tra lai lan nua

# PREDICTION
# format datetime Data
Data['lastupdate'] = pd.to_datetime(Data['lastupdate'],
                              format='%Y-%m-%d',
                              errors='coerce')

DataEncode = Data
DataEncode[DataEncode == 0] = np.nan

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
headers = ["district", "lastupdate", "avg", "pollutant"]
for h in headers:
    DataEncode[h] = le.fit_transform(DataEncode[h]).astype(str)

# feature
feature = DataEncode
feature=feature.drop("avg", axis=1)

feature.head()

# labels
label = DataEncode["avg"]
label.head()

# test and train split
X_train, X_test, y_train, y_test = train_test_split(
    feature, label, test_size=0.3)
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

# plt.plot(range(y_test.shape[0]),y_test,'r.' , label="true")
# plt.plot(range(y_test.shape[0]),y_pred,'g.' , label="prediction")
# plt.legend(loc="best")


print(11111111111)
