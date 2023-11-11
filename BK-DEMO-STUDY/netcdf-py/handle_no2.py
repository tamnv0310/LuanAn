from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
import itertools
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
data = Dataset(dir_path + '/' +
               'netCDFfile/S5P_NRTI_L2__NO2____20210420T064803_20210420T065303_18229_01_010400_20210420T073613.nc')
print(data)

# saving the data to lat, long and no2_data variables
lat = np.asarray(data.groups['PRODUCT'].variables['latitude'][0, :, :])
lon = np.asarray(data.groups['PRODUCT'].variables['longitude'][0, :, :])
no2_data = data.groups['PRODUCT'].variables['nitrogendioxide_tropospheric_column'][0, :, :]
foo = [[0 for _ in range(lat)] for _ in range(lon)]
# no2_min = no2_data.min()
# no2_max = no2_data.max()

# extracting the fill value
fill_value = data.groups['PRODUCT'].variables['nitrogendioxide_tropospheric_column']._FillValue
fill_val = fill_value*1000000

# replacing the fill value/mising value bay 'NAN"
no2_em = np.array(no2_data)*1000000  # micro mol/m-2#
# if currentVal = fillVal ==> currentVal = NAN val#
no2_em[no2_em == fill_val] = np.nan
no2_data = no2_em

#CACH 1
def find_nearest(array, value):
    selected_list = np.empty(shape = (0,2))
    array = np.asarray(array)
    abs_list = np.abs(array - value)
    #epsilon = 5%
    epsilon = 0.05
    res_list = array[abs_list*10000 < epsilon*10000 ]
    for res in res_list:
        x = int(np.where(array[:,:] == res)[0][0])
        y = int(np.where(array[:,:] == res)[1][0])
        selected_list = np.append(selected_list, np.asarray([[x,y]]), axis=0)
    return selected_list

def intsect_2d(array_1, array_2):
    A = np.array(array_1)
    B = np.array(array_2)

    nrows, ncols = A.shape
    dtype={'names':['f{}'.format(i) for i in range(ncols)],
        'formats':ncols * [A.dtype]}

    C = np.intersect1d(A.view(dtype), B.view(dtype))

    # This last bit is optional if you're okay with "C" being a structured array...
    C = C.view(A.dtype).reshape(-1, ncols)
    return C

def dist_between_two_lat_lon(*args):
    from math import asin, cos, radians, sin, sqrt
    lat1, lat2, long1, long2 = map(radians, args)

    dist_lats = abs(lat2 - lat1) 
    dist_longs = abs(long2 - long1) 
    a = sin(dist_lats/2)**2 + cos(lat1) * cos(lat2) * sin(dist_longs/2)**2
    c = asin(sqrt(a)) * 2
    radius_earth = 6378 # the "Earth radius" R varies from 6356.752 km at the poles to 6378.137 km at the equator.
    # print(c * radius_earth,lat2 ,lat1, long2, long1)
    return c * radius_earth

def find_closest_lat_lon(data, v):
    try:
        return min(data, key=lambda p: dist_between_two_lat_lon(v['lat'],v['lon'],p['lat'],p['lon']))
    except TypeError:
        print('Not a list or not a number.')

def find_no2(lat_val,lon_val):
    select_lat = find_nearest(lat, lat_val)
    select_lon = find_nearest(lon, lon_val)
    locations_match = intsect_2d(select_lat, select_lon)
    location_sel_list = np.empty(shape = (0,1))
    for location in locations_match:
        x = int(location[0])
        y = int(location[1])
        location_sel_list = np.append(location_sel_list, {"lat": lat[x,y], "lon": lon[x,y], "x" : x, "y" : y})
    location_to_find = {'lat': lat_val, 'lon': lon_val}
    nearest_location =  find_closest_lat_lon(location_sel_list, location_to_find)
    print(location_sel_list)
    print("Input", location_to_find)
    print("Output (nearest location)", nearest_location)
    res = no2_data[nearest_location["x"],nearest_location["y"]]
    if res:
        return no2_data[nearest_location["x"],nearest_location["y"]]
    return np.nan
