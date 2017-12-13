import pandas as pd
import numpy as np
from math import sin, cos, sqrt, atan2, radians
from dateutil import relativedelta

min_lon = 0.0
min_lat = 0.0
def distance(lat1,lat2, lon1, lon2):
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    dlat = lat2-lat1
    dlon = lon1-lon2
    a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
    return 6373.0 * 2 * atan2(sqrt(a),sqrt(1-a))

                      
def distances(row):
    x = distance(min_lat, row['LATITUDE'], min_lon, min_lon)
    y = distance(min_lat, min_lat, min_lon, row['LONGITUDE'])
    row['X'] = x
    row['Y'] = y
    return row


#test size
data = pd.read_csv("Business_Licenses.tsv", sep='\t')
#get rid of useless data
data = data.loc[:,['LATITUDE','LONGITUDE','LICENSE TERM START DATE','LICENSE TERM EXPIRATION DATE']]
#print the size of db
print(len(data))
#drop all rows with empty cell if presented
#data[['LATITUDE','LONGITUDE']].replace(r'^\s*$', np.nan, regex=True, inplace = True)
data['LICENSE TERM EXPIRATION DATE'] = data['LICENSE TERM EXPIRATION DATE'].fillna('2017-12-15')
data = data.dropna(how='any')
#print current size of db
print(len(data))
#calculate minimum latitude and logitude
data.LATITUDE = data.LATITUDE.astype(float)
data.LONGITUDE = data.LONGITUDE.astype(float)
min_lat = data[['LATITUDE']].min()
min_lon = data[['LONGITUDE']].min()
data = data.apply(distances,axis=1)
#add time frames
data['LICENSE TERM START DATE'] = pd.to_datetime(data['LICENSE TERM START DATE'])
data['LICENSE TERM EXPIRATION DATE'] = pd.to_datetime(data['LICENSE TERM EXPIRATION DATE'])
earliest = data[['LICENSE TERM START DATE']].min()

def timeFrames(row):
    beg = int((row['LICENSE TERM START DATE'] - earliest[0]).days/30.36)
    end = int((row['LICENSE TERM EXPIRATION DATE'] - row['LICENSE TERM START DATE']).days/30.36)
    row['FRAMES'] = ' '.join(map(str,np.arange(start=beg,stop=end+beg,step=1)))
    return row

print(earliest)
data = data.apply(timeFrames,axis=1)
#save to the file
data = data.loc[:,['X','Y','FRAMES']]
data.to_csv("test_dest.csv",sep=',',encoding='utf-8',index=False)
