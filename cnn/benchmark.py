import numpy as np
import pandas as pd
from runner import run  

MSFT_pos = [2, 3, 4, 5]
AAPL_pos = [18, 19, 20, 21]
AMZN_pos = [26, 27, 28, 29]
# Open, High, Low, Close
days_given = 270
days_prediction = 60


data = np.load('./normalisation/data_sliced.npy')
data_norm = np.load('./normalisation/data_sliced_norm.npy')
data = data[:, :, 1:]
data_norm = data_norm[:, : , 1:]
print(data.shape)
final_entry = data.shape[0] - 1
# final_entry = 4200

result_arr = np.zeros((4, days_prediction, final_entry-4000))
real_difference_arr = np.zeros((4, days_prediction, final_entry-4000))
position_arr = np.zeros((4, days_prediction, final_entry-4000))
known_arr = np.zeros((4, final_entry-4000))
for entry in range(4000, final_entry):
    print(entry- 3999)
    data_to_predict = data_norm[entry, 0:days_given, :]
    data_to_predict = data_to_predict[np.newaxis, ...]
    result = run(data=data[entry, :, :], data_to_predict=data_to_predict, ticker='AMZN', result_pos=AMZN_pos)
    for type in range(0, 4):
        result_arr[type, :, entry - 4000] = result[:, type]
        position_arr[type, :, entry - 4000] = result[:, type] - data[entry, days_given - 1, AMZN_pos[type]]
        known_arr[type, entry - 4000] = data[entry, days_given - 1, AMZN_pos[type]]
        real_difference_arr[type, :, entry - 4000] = data[entry, days_given:days_given+days_prediction, AMZN_pos[type]] - data[entry, days_given - 1, AMZN_pos[type]]

position_arr[position_arr < 0] = -1
position_arr[position_arr >= 0 ] = 1
# print(real_difference_arr[3, :, :])
real_difference_arr = np.multiply(real_difference_arr, position_arr)  
# print(position_arr[3, :, :])
final_result_arr = np.zeros((days_prediction, 17))
for day in range(0, days_prediction):
    # print("day: ", day + 1)
    final_result_arr[day, 0] = day + 1
    final_result_arr[day, 1] = np.sum(real_difference_arr[3, day, :]) / (final_entry - 4000)
    final_result_arr[day, 2] = np.sum(real_difference_arr[3, day, :] / known_arr[3, :]) / (final_entry - 4000) * 100 
    # print("% of long ")
    # print(result_arr[3, day, position_arr[3, day, :] > 0 ].shape[0] / result_arr.shape[2] * 100)
    final_result_arr[day, 3] = result_arr[3, day, position_arr[3, day, :] > 0 ].shape[0] / result_arr.shape[2] * 100
    # print("long recognized: ")
    # print(real_difference_arr[3, day, np.logical_and(real_difference_arr[3, day, :] > 0, position_arr[3, day, :] > 0)].shape[0])
    final_result_arr[day, 4] = real_difference_arr[3, day, np.logical_and(real_difference_arr[3, day, :] > 0, position_arr[3, day, :] > 0)].shape[0]
    # print("long unrecognized: ")
    # print(real_difference_arr[3, day, np.logical_and(real_difference_arr[3, day, :] < 0, position_arr[3, day, :] < 0)].shape[0])
    final_result_arr[day, 5] = real_difference_arr[3, day, np.logical_and(real_difference_arr[3, day, :] < 0, position_arr[3, day, :] < 0)].shape[0]
    if(position_arr[3, day, position_arr[3, day, :] > 0].shape[0] > 0):
        # print("best result: ")
        # print(np.max(real_difference_arr[3, day, position_arr[3, day, :] > 0]))
        final_result_arr[day, 6] = np.max(real_difference_arr[3, day, position_arr[3, day, :] > 0])
        # print("average result: ")
        # print(np.sum(real_difference_arr[3, day, position_arr[3, day, :] > 0]) / position_arr[3, day, position_arr[3, day, :] > 0].shape[0])
        final_result_arr[day, 7] = np.sum(real_difference_arr[3, day, position_arr[3, day, :] > 0]) / position_arr[3, day, position_arr[3, day, :] > 0].shape[0]
        # print("average result in %: ")
        # print(np.sum(real_difference_arr[3, day, position_arr[3, day, :] > 0] / known_arr[3, position_arr[3, day, :] > 0]) / position_arr[3, day, position_arr[3, day, :] > 0].shape[0]) * 100
        final_result_arr[day, 8] = np.sum(real_difference_arr[3, day, position_arr[3, day, :] > 0] / known_arr[3, position_arr[3, day, :] > 0]) / position_arr[3, day, position_arr[3, day, :] > 0].shape[0]
        # print("worst result: ")
        # print(np.min(real_difference_arr[3, day, position_arr[3, day, :] > 0]))
        final_result_arr[day, 9] = np.min(real_difference_arr[3, day, position_arr[3, day, :] > 0])

    # print("% of short ")
    # print(result_arr[3, day, position_arr[3, day, :] < 0 ].shape[0] / result_arr.shape[2] * 100)
    final_result_arr[day, 10] = result_arr[3, day, position_arr[3, day, :] < 0 ].shape[0] / result_arr.shape[2] * 100
    # print("short recognized: ")
    # print(real_difference_arr[3, day, np.logical_and(real_difference_arr[3, day, :] > 0, position_arr[3, day, :] < 0)].shape[0])
    final_result_arr[day, 11] = real_difference_arr[3, day, np.logical_and(real_difference_arr[3, day, :] > 0, position_arr[3, day, :] < 0)].shape[0]
    # print("short unrecognized: ")
    # print(real_difference_arr[3, day, np.logical_and(real_difference_arr[3, day, :] < 0, position_arr[3, day, :] > 0)].shape[0])
    final_result_arr[day, 12] = real_difference_arr[3, day, np.logical_and(real_difference_arr[3, day, :] < 0, position_arr[3, day, :] > 0)].shape[0]
    if(position_arr[3, day, position_arr[3, day, :] < 0].shape[0] > 0):
        # print("best result: ")
        # print(np.max(real_difference_arr[3, day, position_arr[3, day, :] < 0]))
        final_result_arr[day, 13] = np.max(real_difference_arr[3, day, position_arr[3, day, :] < 0])
        # print("average result: ")
        # print(np.sum(real_difference_arr[3, day, position_arr[3, day, :] < 0]) / position_arr[3, day, position_arr[3, day, :] < 0].shape[0])
        final_result_arr[day, 14] = np.sum(real_difference_arr[3, day, position_arr[3, day, :] < 0]) / position_arr[3, day, position_arr[3, day, :] < 0].shape[0]
        # print("average result in %: ")
        # print(np.sum(real_difference_arr[3, day, position_arr[3, day, :] < 0] / known_arr[3, position_arr[3, day, :] < 0]) / position_arr[3, day, position_arr[3, day, :] < 0].shape[0]) * 100
        final_result_arr[day, 15] = np.sum(real_difference_arr[3, day, position_arr[3, day, :] < 0] / known_arr[3, position_arr[3, day, :] < 0]) / position_arr[3, day, position_arr[3, day, :] < 0].shape[0]
        # print("worst result: ")
        # print(np.min(real_difference_arr[3, day, position_arr[3, day, :] < 0]))
        final_result_arr[day, 16] = np.min(real_difference_arr[3, day, position_arr[3, day, :] < 0])

df = pd.DataFrame(final_result_arr, columns=['day', 'average result', 'average result %', '% of long', 'long recognized', 'long unrecognized', 'best result long', 'average result long', 'average result long %', 'worst result long',
                                             '% of short', 'short recognized', 'short unrecognized', 'best result short', 'average result short', 'average result short %', 'worst result short'])

df.to_excel('./cnn/benchmark_res.xlsx')