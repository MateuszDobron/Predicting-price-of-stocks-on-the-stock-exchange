import sys
import pandas as pd
import numpy as np

data = pd.read_csv('./dataset/dataset.csv')
print(data.columns)
data.drop(columns="Year", inplace=True)
data_np = data.to_numpy()
print(data_np.shape)

for col in range(0, data_np.shape[1]):
    for row in range(0, data_np.shape[0]):
                if np.isnan(data_np[row, col]):
                    print(row, ' ', col)
                    print(data_np[row, col])
                    print(data_np[row - 1, col])
                    print('nan entry in dataset')

companies = ["AAPL", "MSFT", "AMZN", "GOOG", "NVDA"]
values = ["_Open", "_High", "_Low", "_Close", "_Volume", '_EPS'] 
financial_ind = ['_ROE', '_ROA']

columns_to_normalise = list()
columns_from_normalise_full = list()

for company in companies:
    for value in values:
        columns_to_normalise.append(company+value)
    for ind in financial_ind:
        columns_from_normalise_full.append(company+ind)

columns_from_normalise_full.append('CPI')
columns_from_normalise_full.append('2 Yr')
columns_from_normalise_full.append('20 Yr')
columns_from_normalise_full_int = list()

i = 0
for column in data.columns:
    for column_from_normalise in columns_from_normalise_full:
        if column == column_from_normalise:
            columns_from_normalise_full_int.append(i)
    # if(i == 34):
    #     print(column.title())
    # if(i == 45):
    #     print(column.title())
    i += 1

days_to_learn = 3700
days_given = 270
days_prediction = 60

for column_int in columns_from_normalise_full_int:
    if(np.max(data_np[:(days_to_learn + days_given + days_prediction), column_int]) - np.min(data_np[:(days_to_learn + days_given + days_prediction), column_int]) == 0):
        data_np[:, column_int] = 1.5
    else:
        data_np[:, column_int] = (data_np[:, column_int] - np.min(data_np[:(days_to_learn + days_given + days_prediction), column_int])) / (np.max(data_np[:(days_to_learn + days_given + days_prediction), column_int]) - np.min(data_np[:(days_to_learn + days_given + days_prediction), column_int])) + 1

data_sliced = np.zeros((days_given + days_prediction, data_np.shape[1], data_np.shape[0] - days_given - days_prediction + 1))
# print(days_given + days_prediction)
# print(data_sliced.shape)

for i in range(0, data_np.shape[0] - days_given - days_prediction + 1):
    data_sliced[:, :, i] = data_np[i:i + days_given + days_prediction, :]

print(data_sliced.shape)
np.set_printoptions(threshold=sys.maxsize)
# print(data_sliced[:, 0:3 , 4494])

columns_to_normalise.append("M1")
columns_to_normalise.append("M2")

columns_to_normalise_int = list()
to_predict = list()

i = 0
for column in data.columns:
    for column_from_normalise in columns_to_normalise:
        if column == column_from_normalise:
            columns_to_normalise_int.append(i)
    if column in ('AMZN_Open', 'AMZN_High', 'AMZN_Low', 'AMZN_Close'):
        to_predict.append(i)
    i += 1

# print(columns_to_normalise_int)
print('before slice normalization', data_sliced.shape)

data_sliced_norm = data_sliced.copy()
for i in range(0, data_sliced.shape[2]):
    for column in columns_to_normalise_int:
        if(np.max(data_sliced[:days_to_learn, column, i]) - np.min(data_sliced[:days_to_learn, column, i]) == 0):
            data_sliced_norm[:, column, i] = 1.5
        else:
            data_sliced_norm[:, column, i] = (data_sliced[:, column, i] - np.min(data_sliced[:days_to_learn, column, i])) / (np.max(data_sliced[:days_to_learn, column, i]) - np.min(data_sliced[:days_to_learn, column, i])) + 1

data_sliced = np.transpose(data_sliced, (2, 0, 1))
data_sliced_norm = np.transpose(data_sliced_norm, (2, 0, 1))

print(data_sliced.shape)
print(data_sliced_norm.shape)
print('columns to predict', to_predict)
print(data_sliced_norm[0, 0, :])

np.save('./normalisation/data_sliced_norm.npy', data_sliced_norm)
np.save('./normalisation/data_sliced.npy', data_sliced)
np.save('./normalisation/topredict.npy', to_predict)
