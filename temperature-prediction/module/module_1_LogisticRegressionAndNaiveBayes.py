#import library packages
import pandas as p
import matplotlib.pyplot as plt
import seaborn as s
import numpy as n

import warnings
warnings.filterwarnings("ignore")

dataset_path = "air-quality-dataset/_DISTRICT-ALL/hcm-3.csv"

# Loading dataset using pandas
df = p.read_csv(dataset_path)

df.columns

from sklearn.preprocessing import LabelEncoder
var_mod = ["district", "lastupdate", "avg", "pollutant"]
le = LabelEncoder()
for i in var_mod:
    df[i] = le.fit_transform(df[i]).astype(str)
