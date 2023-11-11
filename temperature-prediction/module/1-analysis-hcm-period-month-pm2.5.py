import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import datetime as dt

# Loading dataset using pandas
Data = pd.read_csv('air-quality/temperature-prediction/module/dataset/lanh-su-quan-hoa-ky-hcm-pm2.5.csv')
Data['date'] = pd.to_datetime(Data['date'],
                              format='%Y-%m-%d',
                              errors='coerce')

Data = Data[Data['date'] >= '2021-01-21 00:00:00']
Data = Data[Data['date'] <= '2021-04-05 00:00:00']
Data["year"] = Data["date"].dt.year
Data["month"] = Data["date"].dt.month
Data["day"] = Data["date"].dt.day

_avg = Data.groupby(pd.PeriodIndex(Data['date'], freq="M"))['pm2.5'].mean()
_min = Data.groupby(pd.PeriodIndex(Data['date'], freq="M"))['pm2.5'].min()
_max = Data.groupby(pd.PeriodIndex(Data['date'], freq="M"))['pm2.5'].max()


months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
_idxs = []
_pm25 = {"avg": [], "max": [], "min": []}

for idx in range(len(_avg)):
    _idxs.append(months[idx])
    _pm25["avg"].append(_avg[idx])
    _pm25["max"].append(_max[idx])
    _pm25["min"].append(_min[idx])

fig, (ax1) = plt.subplots(1,1, figsize=(5, 4), sharex=False, dpi=120)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.35, hspace=0.3)

ax1.plot(_idxs, _pm25["max"], 'r.-', label="max")
ax1.plot(_idxs, _pm25["avg"], 'ys-', label="avg")
ax1.plot(_idxs, _pm25["min"], 'gx-', label="min")
ax1.set(title="PM2.5", xlabel="months", ylabel="µg/m3")
ax1.legend(loc="best")

# plt.suptitle("PM2.5 in Ho Chi Minh City - Lanh Su Quan Hoa Ky (January to April, 2021)")
plt.show()

print("Complete")