import numpy as np

def get_data():
    f = open("train.csv")
    f.seek(0,0)
    
    matrix = [np.array(i.split(',')) for i in f.read().split('\n')][:-1]
    return matrix


m = get_data()

for i in m:
    if len(i) != 625:
       print(len(i))

print("Done")
