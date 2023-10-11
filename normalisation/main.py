import sys
import pandas as pd
import numpy as np

data = pd.read_csv('./dataset/dataset.csv')
for column in data.columns:
    data[column] = data[column].astype(str)
    data[column] = data[column].str.replace("$", "")
    data[column] = data[column].str.replace(",", ".")
    data[column] = data[column].astype(float)
print(data.columns)
data.drop(columns="Year", inplace=True)
data_np = data.to_numpy()
print(data_np.shape)

days_given = 180
days_prediction = 60
data_sliced = np.zeros((days_given + days_prediction, data_np.shape[1], data_np.shape[0] - days_given - days_prediction + 1))
print(days_given + days_prediction)
print(data_sliced.shape)

for i in range(0, data_np.shape[0] - days_given - days_prediction + 1):
    data_sliced[:, :, i] = data_np[i:i + days_given + days_prediction, :]

print(data_sliced.shape)
np.set_printoptions(threshold=sys.maxsize)
print(data_sliced[:, 0:3 , 4489])