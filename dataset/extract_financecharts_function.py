import pandas as pd
import os

def extract_financecharts(column_to_extract, max_column, extract_column_name, ticker):
    path_default = './dataset/data/'
    path = path_default + ticker + '/' + ticker + '_' + extract_column_name
    if os.path.exists(path + '.csv'):
        os.remove(path + '.csv')
    file = open(path + '.txt')
    lines = file.readlines()
    count = 0
    day = []
    month = []
    year = []
    data = []
    correct_dates = pd.read_csv(path_default + ticker + '/dates.csv')
    i = 0
    for line in lines:
        line = line.rstrip('\n')
        if count == 0:
            line = line.split(sep='/')
            day.append(correct_dates["Day"].iloc[i])
            month.append(correct_dates["Month"].iloc[i])
            year.append(correct_dates["Year"].iloc[i])
            i += 1
        if count == column_to_extract:
            if line[0] == "$":
                line = line.lstrip('$')
            line = line.replace(',', '')
            data.append(line)
        if count == max_column:
            count = 0
        else:
            count += 1
    result = pd.DataFrame(list(zip(year, month, day, data)), columns=['Year', 'Month', 'Day', extract_column_name])
    result.to_csv(path + '.csv')
    file.close()
