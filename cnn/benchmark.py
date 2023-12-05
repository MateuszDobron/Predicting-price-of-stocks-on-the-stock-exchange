import numpy as np
import pandas as pd
import tensorflow as tf

days_given = 500
days_prediction = 90

data = np.load('./cnn/data/data_sliced.npy')
data_norm = np.load('./cnn/data/data_sliced_norm.npy')
to_predict = np.load('./cnn/data/topredict.npy')
to_predict = to_predict - 2
data = data[:, :, 2:]
data_norm = data_norm[:, : , 2:]
print(data.shape)
final_entry = data.shape[0]
start_entry = 3750
# final_entry = 3760

def run_benchark():
    model = tf.keras.models.load_model('./cnn/model.keras')
    result_arr = np.zeros((final_entry - start_entry, days_prediction, to_predict.shape[0]))
    result_arr_denorm = np.zeros((final_entry - start_entry, days_prediction, to_predict.shape[0]))

    for slice_number in range(start_entry, final_entry):
        data_to_predict = data_norm[slice_number, :days_given, :]
        data_to_predict = data_to_predict[np.newaxis, ...]
        result = model(data_to_predict)
        for indicator in range(0, to_predict.shape[0]):
            result_arr[slice_number - start_entry, :, indicator] = result[0, indicator * days_prediction:(indicator + 1) * days_prediction]
            if(indicator == 3 and slice_number == start_entry):
                print(result[0, indicator * days_prediction:(indicator + 1) * days_prediction])
            result_arr_denorm[slice_number - start_entry, :, indicator] = (result_arr[slice_number - start_entry, :, indicator] - 1) * (np.max(data[slice_number, :days_given, to_predict[indicator]]) - np.min(data[slice_number, :days_given, to_predict[indicator]])) + np.min(data[slice_number, :days_given, to_predict[indicator]])

    difference_arr = np.zeros((final_entry - start_entry, days_prediction, to_predict.shape[0]))
    real_difference_arr = np.zeros((final_entry - start_entry, days_prediction, to_predict.shape[0]))

    for day in range(0, days_prediction):   
        difference_arr[:, day, :] = result_arr_denorm[:, day, :] - data[start_entry:final_entry, days_given - 1, to_predict] #predicted - known
        real_difference_arr[:, day, :] = data[start_entry:final_entry, days_given + day, to_predict] - data[start_entry:final_entry, days_given - 1, to_predict] # future - known

    # print(difference_arr.shape)
    # print(result_arr[:, 50, 3])
    # print(result_arr_denorm[:, 50, 3])
    # print(difference_arr[:, 50, 3])

    position_arr = difference_arr.copy()    
    position_arr[position_arr < 0] = -1
    position_arr[position_arr >= 0 ] = 1
    result_arr = np.multiply(position_arr, real_difference_arr)
    final_result_arr = np.zeros((days_prediction, 9))

    companies_list = ['MSFT', 'NVDA', 'AAPL', 'AMZN', 'AMD']
    for company in range(0, 5):
        for day in range(0, days_prediction):
    #         print("day: ", day + 1)
            final_result_arr[day, 0] = day + 1
            final_result_arr[day, 1] = np.sum(result_arr[:, day, company * 4 + 3]) / (final_entry - start_entry)
            final_result_arr[day, 2] = np.sum(result_arr[:, day, company * 4 + 3] / data[start_entry:final_entry, days_given - 1, to_predict[company * 4 + 3]]) / (final_entry - start_entry) * 100 
    #         print("% of long ")
            final_result_arr[day, 3] = position_arr[position_arr[:, day, company * 4 + 3] > 0, day, company * 4 + 3].shape[0] / (final_entry - start_entry) * 100
        #     # print("long recognized: ")
            final_result_arr[day, 4] = position_arr[np.logical_and(position_arr[:, day, company * 4 + 3] > 0, real_difference_arr[:, day, company * 4 + 3] > 0), day, company * 4 + 3].shape[0]
        #     # print("long unrecognized: ")
            final_result_arr[day, 5] = position_arr[np.logical_and(position_arr[:, day, company * 4 + 3] < 0, real_difference_arr[:, day, company * 4 + 3] > 0), day, company * 4 + 3].shape[0]
        #     # print("% of short ")
            final_result_arr[day, 6] = position_arr[position_arr[:, day, company * 4 + 3] < 0, day, company * 4 + 3].shape[0] / (final_entry - start_entry) * 100
        #     # print("short recognized: ")
            final_result_arr[day, 7] = position_arr[np.logical_and(position_arr[:, day, company * 4 + 3] < 0, real_difference_arr[:, day, company * 4 + 3] < 0), day, company * 4 + 3].shape[0]
        #     # print("short unrecognized: ")
            final_result_arr[day, 8] = position_arr[np.logical_and(position_arr[:, day, company * 4 + 3] > 0, real_difference_arr[:, day, company * 4 + 3] < 0), day, company * 4 + 3].shape[0]

        df = pd.DataFrame(final_result_arr, columns=['day', 'average result', 'average result %', '% of long', 'long recognized', 'long unrecognized', '% of short', 'short recognized', 'short unrecognized'])
        df.to_excel('./cnn/benchmark_results/' + companies_list[company] + '.xlsx')
