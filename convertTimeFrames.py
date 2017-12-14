import numpy as np
import pandas as pd


#define size of heap
size = 25
#define size of a block 1x1
dim = 2

data = pd.read_csv('test_dest.csv')
data = data.dropna(how='any')
data['X'] = pd.to_numeric(data['X'])
data['Y'] = pd.to_numeric(data['Y'])
points = np.array([np.zeros(size*size)])
for index,row in data.iterrows():
    block = int((row['Y'] * size + row['X'])/2)
    frames = np.array(row['FRAMES'].split(' '),dtype=int)
    #if we have new frames. extend number of datapoints
    if frames[-1] >= len(points):
        for i in range(len(points),frames[-1]+1):
            points = np.vstack([points,np.zeros(size*size)])
    #now add each datapoint
    for t in frames:
        points[t][block] += 1

#save the result
data = pd.DataFrame(data=points[1:,1:],
                    index=points[1:,0],
                    columns=points[0,1:])
data.to_csv("train.csv")
