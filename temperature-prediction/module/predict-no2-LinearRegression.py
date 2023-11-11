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

# Loading dataset using pandas
Data = pd.read_csv(dataset_path + "hcm-2" + ".csv")

#Tien xu ly du lieu
num = Data._get_numeric_data()
num[num < 0] = 0

# Kiem tra (checking) va dem so luong (counting) du lieu mat mat (missing data) cho moi cot (column)
Data.isnull().sum()

# Xoa gia tri mat mat (Deleting missing values)
DataCleaned = Data.dropna()
DataCleaned.isnull().sum()  # kiem tra lai lan nua

# Exploration : mo rong
# #Creating Dataset
# np.random.seed(10)
# _data = Data["no2"]
# print("====== data \n", _data)
# fig = plt.figure(figsize=(10, 7))

# #creating a plot
# plt.boxplot(_data)

# #show plot
# plt.show()

# from pandas_visual_analysis import VisualAnalysis
# VisualAnalysis(Data)

# #Ma tran tuong quan (Correlation matrix)
# corrmat = Data.corr()
# top_corr_feature = corrmat.index
# plt.figure(figsize=(10,7))

# to plot headmap
# g = sns.heatmap(Data[top_corr_feature].corr(), annot=True,cmap="viridis")

# #paitplot
# sns.pairplot(Data)

# #histogram
# Data["no2"].plot.hist()

# #Bieu do phan tan
# Data.plot(kind="scatter", x="no2", y="co")
# plt.show()

# PREDICTION
# format datetime Data
Data['date'] = pd.to_datetime(Data['date'],
                              format='%Y-%m-%d',
                              errors='coerce')

# feature
feature = Data
feature["no2"] = feature["no2"]*1000000 #micro mol/m2
feature["year"] = feature["date"].dt.year
feature["month"] = feature["date"].dt.month
#feature["week"] = feature["date"].dt.week
feature["day"] = feature["date"].dt.day
feature["no"] = feature["date"].dt.day
#feature["dayofweek"] = feature["date"].dt.dayofweek
feature=feature.drop("date", axis=1)
feature=feature.drop("dist", axis=1)
feature=feature.drop("co", axis=1)
feature=feature.drop("no2", axis=1)
feature=feature.drop("o3", axis=1)
feature=feature.drop("so2", axis=1)
feature=feature.drop("ch4", axis=1)
feature=feature.drop("hcho", axis=1)

feature.head()

# labels
label = Data["no2"]
label.head()

# test and train split
X_train, X_test, y_train, y_test = train_test_split(
    feature, label, test_size=0.1)
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

plt.plot(range(y_test.shape[0]),y_test,'r.' , label="true")
plt.plot(range(y_test.shape[0]),y_pred,'g.' , label="prediction")
plt.legend(loc="best")


print(11111111111)
