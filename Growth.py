import numpy as np


def growth(data):
    s = np.sum([(data[i+1]-data[i])/data[i] for i in range(len(data)-1)])
    return s/(len(data)-1)
