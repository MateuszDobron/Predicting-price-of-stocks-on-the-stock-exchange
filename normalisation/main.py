import sys
import pandas as pd
import numpy as np

data = pd.read_csv('./dataset/dataset.csv')
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

company_to_predict = "AAPL"
companies = ["AAPL", "MSFT", "AMZN", "GOOG", "NVDA"]
values = ["_Open", "_High", "_Low", "_Close", "_Volume"]
columns_to_normalise = list()

for company in companies:
    for value in values:
        columns_to_normalise.append(company+value)

columns_to_normalise.append("M1")
columns_to_normalise.append("M2")

columns_to_normalise_int = list()

i = 0
for column in data.columns:
    for column_from_normalise in columns_to_normalise:
        if column == column_from_normalise:
            columns_to_normalise_int.append(i - 1)
    i += 1

print(columns_to_normalise_int)


print(data_sliced.shape)
data_sliced_norm = data_sliced.copy()
for i in range(0, data_sliced.shape[2]):
    for column in columns_to_normalise_int:
        if(np.max(data_sliced[:, column, i]) - np.min(data_sliced[:, column, i]) == 0):
            data_sliced_norm[:, column, i] = 0.5
        else:
            data_sliced_norm[:, column, i] = (data_sliced[:, column, i] - np.min(data_sliced[:, column, i])) / (np.max(data_sliced[:, column, i]) - np.min(data_sliced[:, column, i]))

np.save('./normalisation/data_sliced_norm.npy', data_sliced_norm)
np.save('./normalisation/data_sliced.npy', data_sliced)

