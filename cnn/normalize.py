import sys
import pandas as pd
import numpy as np

def normalize():
    data = pd.read_csv('./dataset/dataset.csv')
    print(data.columns)
    # data.drop(columns="Year", inplace=True)
    data_np = data.to_numpy()
    print(data_np.shape)

    for col in range(0, data_np.shape[1]):
        for row in range(0, data_np.shape[0]):
                    if np.isnan(data_np[row, col]):
                        print(row, ' ', col)
                        print(data_np[row, col])
                        print(data_np[row - 1, col])
                        print('nan entry in dataset')
                        data_np[row, col] = data_np[row - 1, col]

    companies = ["MSFT", "NVDA", "AAPL", "AMZN", "AMD"]
    values = ["_Open", "_High", "_Low", "_Close", "_Volume", '_EPS', '_ROE', '_ROA'] 

    columns_to_normalise = list()

    for company in companies:
        for value in values:
            columns_to_normalise.append(company+value)

    columns_to_normalise.append('CPI')
    columns_to_normalise.append('2 Yr')
    columns_to_normalise.append('20 Yr')
    columns_to_normalise.append("M1")
    columns_to_normalise.append("M2")

    days_to_learn = 3200
    days_given = 500
    days_prediction = 90

    data_sliced = np.zeros((days_given + days_prediction, data_np.shape[1], data_np.shape[0] - days_given - days_prediction + 1))
    # print(days_given + days_prediction)
    # print(data_sliced.shape)

    for i in range(0, data_np.shape[0] - days_given - days_prediction + 1):
        data_sliced[:, :, i] = data_np[i:i + days_given + days_prediction, :]

    print(data_sliced.shape)
    np.set_printoptions(threshold=sys.maxsize)
    # print(data_sliced[:, 0:3 , 4494])

    columns_to_normalise_int = list()
    indicators_to_predict = ["_Open", "_High", "_Low", "_Close"]
    to_predict = list()

    i = 0
    for column in data.columns:
        for column_from_normalise in columns_to_normalise:
            if column == column_from_normalise:
                columns_to_normalise_int.append(i)
        for company in companies:
            for indicator_to_predict in indicators_to_predict:
                # print(column)
                # print(company + indicator_to_predict)
                if column == company + indicator_to_predict:
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

    np.save('./cnn/data/data_sliced_norm.npy', data_sliced_norm)
    np.save('./cnn/data/data_sliced.npy', data_sliced)
    np.save('./cnn/data/topredict.npy', to_predict)
    np.save('./cnn/data/tonormalize.npy', columns_to_normalise_int)
