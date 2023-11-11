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
    "q11": [10.76362650241118, 106.64765485576544, 203, 214, 11],
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

Data = Data[Data['date'] >= '2021-01-01 00:00:00']
Data = Data[Data['date'] <= '2021-01-31 00:00:00']
Data["year"] = Data["date"].dt.year
Data["month"] = Data["date"].dt.month
Data["day"] = Data["date"].dt.day

#plt.plot(Data["date"], Data["no2"])

# #filter by district
# for dist in dist_list:
#     dist_list[dist] = Data[Data["dist"] ==  dist]

# #group by month and caculating avg
# for dist in dist_list:
#     _data = dist_list[dist].groupby(pd.PeriodIndex(dist_list[dist]['date'], freq="M"))['co'].mean()
#     _min = dist_list[dist].groupby(pd.PeriodIndex(dist_list[dist]['date'], freq="M"))['co'].min()
#     _max = dist_list[dist].groupby(pd.PeriodIndex(dist_list[dist]['date'], freq="M"))['co'].max()
#     fig, ax = plt.subplots()
#     _data.plot(ax=ax, label="avg")
#     _min.plot(ax=ax, label="min")
#     _max.plot(ax=ax, label="max")
#     ax.set(title="Carbon monoxide")
#     plt.show()
#     break

#filterDataNo2 = Data[Data.no2>0]

# _data = Data.groupby(pd.PeriodIndex(Data['date'], freq="D"))['co', 'no2', 'o3', 'so2', 'ch4','hcho'].mean()


_data = Data.loc[Data['dist'] == 'q1']
_data = _data.reset_index(drop=True) #reset index after loc
print(_data)
_idxs = []
_co = []
_no2 = []
_o3 = []
_so2 = []
_ch4 = []
_hcho = []
for idx, val in enumerate(_data["co"]):
    print(idx, val)
    _idxs.append(idx+1)
    _co.append(_data["co"][idx]*1000000)
    _no2.append(_data["no2"][idx]*1000000)
    _o3.append(_data["o3"][idx]*1000000)
    _so2.append(_data["so2"][idx]*1000000)
    _ch4.append(_data["ch4"][idx]*1000000)
    _hcho.append(_data["hcho"][idx]*1000000)



fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(100, 8), sharex=False, dpi=120)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.35, hspace=0.3)

ax1.plot(_idxs, _co, 'b.-', markersize=3.25, label="density")
ax1.set(title="Carbon monoxide - CO", xlabel="days", ylabel="µmol/m2")
ax1.legend(loc="best")
ax1.set_ylim([-0.05*1000000,0.42*1000000])

ax2.plot(_idxs, _no2, 'b.-', markersize=3.25, label="density")
ax2.set(title="Nitrogen monoxide - NO2", xlabel="days", ylabel="µmol/m2")
ax2.legend(loc="best")
ax2.set_ylim([-0.001*1000000,0.005*1000000])

ax3.plot(_idxs, _o3, 'b.-', markersize=3.25, label="density")
ax3.set(title="Ozone - O3", xlabel="days", ylabel="µmol/m2")
ax3.legend(loc="best")
ax3.set_ylim([0,0.4*1000000])

ax4.plot(_idxs, _so2, 'b.-', markersize=3.25, label="density")
ax4.set(title="Sulfur dioxide - SO2", xlabel="days", ylabel="µmol/m2")
ax4.legend(loc="best")
ax4.set_ylim([-0.02*1000000,0.05*1000000])

ax5.plot(_idxs, _ch4, 'b.-', markersize=3.25, label="density")
ax5.set(title="Methane - CH4", xlabel="days", ylabel="parts per billion")
ax5.legend(loc="best")
ax5.set_ylim([-0.042*1000000,0.1*1000000])

ax6.plot(_idxs, _hcho, 'b.-', markersize=3.25, label="density")
ax6.set(title="Formaldehyde - HCHO", xlabel="days", ylabel="µmol/m2")
ax6.legend(loc="best")
ax6.set_ylim([-0.001*1000000,0.003*1000000])

plt.suptitle("Air Quality in Ho Chi Minh City (January, 1 to 31, 2021)")
plt.show()



print("Complete")