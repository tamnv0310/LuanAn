import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import datetime as dt

# Loading dataset using pandas
Data = pd.read_csv("air-quality/temperature-prediction/module/dataset/lanh-su-quan-hoa-ky-hcm-pm2.5.csv")
Data['date'] = pd.to_datetime(Data['date'],
                              format='%Y-%m-%d',
                              errors='coerce')

Data = Data[Data['date'] >= '2021-03-01 00:00:00']
Data = Data[Data['date'] <= '2021-03-31 00:00:00']
Data["year"] = Data["date"].dt.year
Data["month"] = Data["date"].dt.month
Data["day"] = Data["date"].dt.day

Data = Data.reset_index(drop=True) #reset index after loc

_idxs = []
_pm25 = []
for idx in range(len(Data)):
    _idxs.append(idx+1)
    _pm25.append(Data["pm2.5"][idx])

fig, (ax1) = plt.subplots(1,1, figsize=(4.2, 3.6), sharex=False, dpi=120)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.35, hspace=0.3)

ax1.plot(_idxs, _pm25, 'b.-', markersize=3.25, label="density")
ax1.set(title="PM2.5", xlabel="days", ylabel="µg/m3")
ax1.legend(loc="best")
ax1.set_ylim([0,300])

# plt.suptitle("Air Quality in Ho Chi Minh City (January, 1 to 31, 2021)")
plt.show()


print("Complete")