import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import datetime as dt

dist_list = {
    "q1": [10.780612857979111, 106.69929097226942, 194, 255, 1],
    "q2": [10.783647660067732, 106.72673471144276, 192, 275, 2],
    "q3": [10.782833128986498, 106.68617895544911, 193, 245, 3],
    "q4": [10.766619604634025, 106.70496162697751, 201, 259, 4],
    "q5": [10.755963008464605, 106.66749108555408, 207, 232, 5],
    "q6": [10.746598181717706, 106.64917765698283, 212, 218, 6],
    "q7": [10.73233643049728, 106.72664202853471, 219, 275, 7],
    "q8": [10.740319883142194, 106.66541075067252, 215, 230, 8],
    "q9": [10.83982108902878, 106.77095208740852, 164, 308, 9],
    "q10": [10.767918838830244, 106.66659593804623, 201, 231, 10],
    "q11": [10.763904275145594, 106., 203, 214, 11],
    "q12": [10.86324605768756, 106.65438133369516, 151, 222, 12],
    "qbthanh": [10.803446284783773, 106.69630236758046, 182, 253, 13],
    "qbtan": [10.737193840613681, 106.61566486228712, 216, 193, 14],
    "qgvap": [10.831931525946937, 106.66930567480965, 168, 233, 15],
    "qpnhuan": [10.795230097898482, 106.67533732496804, 186, 237, 16],
    "qtbinh": [10.797934622453923, 106.64237067817248, 185, 213, 17],
    "qtphu": [10.783538492749958, 106.63690663160116, 193, 209, 18],
    "hbchanh": [10.689936987473937, 106.5841934376312, 241, 170, 19],
    "hcgio": [10.411275219925006, 106.95473231899838, 384, 445, 20],
    "hcchi": [10.973555815067174, 106.4938085691552, 95, 103, 21],
    "hhmon": [10.889499705704482, 106.59518769231617, 138, 178, 22],
    "hnbe": [10.674384007461548, 106.73295641257327, 249, 280, 23],
    "tptduc": [10.775752803095694, 106.7544347021429, 197, 296, 24]
}

dataset_path = "air-quality-dataset/_DISTRICT-ALL/"

# Loading dataset using pandas
Data = pd.read_csv(dataset_path + "hcm-2" + ".csv")
Data['date'] = pd.to_datetime(Data['date'],
                              format='%Y-%m-%d',
                              errors='coerce')
Data = Data[Data['date'] > '2018-04-30 00:00:00']
Data["year"] = Data["date"].dt.year
Data["month"] = Data["date"].dt.month
Data["day"] = Data["date"].dt.day

#plt.plot(Data["date"], Data["no2"])

# #filter by district
# for dist in dist_list:
#     dist_list[dist] = Data[Data["dist"] ==  dist]

# #group by month and caculating avg
# for dist in dist_list:
#     _avg = dist_list[dist].groupby(pd.PeriodIndex(dist_list[dist]['date'], freq="M"))['co'].mean()
#     _min = dist_list[dist].groupby(pd.PeriodIndex(dist_list[dist]['date'], freq="M"))['co'].min()
#     _max = dist_list[dist].groupby(pd.PeriodIndex(dist_list[dist]['date'], freq="M"))['co'].max()
#     fig, ax = plt.subplots()
#     _avg.plot(ax=ax, label="avg")
#     _min.plot(ax=ax, label="min")
#     _max.plot(ax=ax, label="max")
#     ax.set(title="Carbon monoxide")
#     plt.show()
#     break

#filterDataNo2 = Data[Data.no2>0]

_avg = Data.groupby(pd.PeriodIndex(Data['date'], freq="M"))['co', 'no2', 'o3', 'so2', 'ch4','hcho'].mean()
_min = Data.groupby(pd.PeriodIndex(Data['date'], freq="M"))['co', 'no2', 'o3', 'so2', 'ch4','hcho'].min()
_max = Data.groupby(pd.PeriodIndex(Data['date'], freq="M"))['co', 'no2', 'o3', 'so2', 'ch4','hcho'].max()

_idxs = []
_co = {"avg": [], "max": [], "min": []}
_no2 = {"avg": [], "max": [], "min": []}
_o3 = {"avg": [], "max": [], "min": []}
_so2 = {"avg": [], "max": [], "min": []}
_ch4 = {"avg": [], "max": [], "min": []}
_hcho = {"avg": [], "max": [], "min": []}

for idx, val in enumerate(_avg["co"]):
    _idxs.append(idx)
    _co["avg"].append(_avg["co"][idx])
    _no2["avg"].append(_avg["no2"][idx])
    _o3["avg"].append(_avg["o3"][idx])
    _so2["avg"].append(_avg["so2"][idx])
    _ch4["avg"].append(_avg["ch4"][idx])
    _hcho["avg"].append(_avg["hcho"][idx])

    _co["min"].append(_min["co"][idx])
    _no2["min"].append(_min["no2"][idx])
    _o3["min"].append(_min["o3"][idx])
    _so2["min"].append(_min["so2"][idx])
    _ch4["min"].append(_min["ch4"][idx])
    _hcho["min"].append(_min["hcho"][idx])

    _co["max"].append(_max["co"][idx])
    _no2["max"].append(_max["no2"][idx])
    _o3["max"].append(_max["o3"][idx])
    _so2["max"].append(_max["so2"][idx])
    _ch4["max"].append(_max["ch4"][idx])
    _hcho["max"].append(_max["hcho"][idx])



fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(24, 8), sharex=True, dpi=120)

ax1.plot(_idxs, _co["max"], 'r.-', label="max")
ax1.plot(_idxs, _co["avg"], 'ys-', label="avg")
ax1.plot(_idxs, _co["min"], 'gx-', label="min")
ax1.set(title="Carbon monoxide - CO", xlabel="months", ylabel="mol/m2")
ax1.legend(loc="best")

ax2.plot(_idxs, _no2["max"], 'r.-', label="max")
ax2.plot(_idxs, _no2["avg"], 'ys-', label="avg")
ax2.plot(_idxs, _no2["min"], 'gx-', label="min")
ax2.set(title="Nitrogen monoxide - NO2", xlabel="months", ylabel="mol/m2")
ax2.legend(loc="best")

ax3.plot(_idxs, _o3["max"], 'r.-', label="max")
ax3.plot(_idxs, _o3["avg"], 'ys-', label="avg")
ax3.plot(_idxs, _o3["min"], 'gx-', label="min")
ax3.set(title="Ozone - O3", xlabel="months", ylabel="mol/m2")
ax3.legend(loc="best")

ax4.plot(_idxs, _so2["max"], 'r.-', label="max")
ax4.plot(_idxs, _so2["avg"], 'ys-', label="avg")
ax4.plot(_idxs, _so2["min"], 'gx-', label="min")
ax4.set(title="Sulfur dioxide - SO2", xlabel="months", ylabel="mol/m2")
ax4.legend(loc="best")

ax5.plot(_idxs, _ch4["max"], 'r.-', label="max")
ax5.plot(_idxs, _ch4["avg"], 'ys-', label="avg")
ax5.plot(_idxs, _ch4["min"], 'gx-', label="min")
ax5.set(title="Methane - CH4", xlabel="months", ylabel="parts per billion")
ax5.legend(loc="best")

ax6.plot(_idxs, _hcho["max"], 'r.-', label="max")
ax6.plot(_idxs, _hcho["avg"], 'ys-', label="avg")
ax6.plot(_idxs, _hcho["min"], 'gx-', label="min")
ax6.set(title="Formaldehyde - HCHO", xlabel="months", ylabel="mol/m2")
ax6.legend(loc="best")

plt.suptitle("Air Quality in Ho Chi Minh City (May, 2018 to August, 2021)")
plt.show()



print(12345678)