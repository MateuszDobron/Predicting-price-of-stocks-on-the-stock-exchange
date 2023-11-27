import pandas as pd
import os

def extract_financecharts(path, column_to_extract, max_column, extract_column_name):
    if os.path.exists(path + '.csv'):
        os.remove(path + '.csv')
    file = open(path + '.txt')
    lines = file.readlines()
    count = 0
    day = []
    month = []
    year = []
    data = []
    for line in lines:
        line = line.rstrip('\n')
        if count == 0:
            line = line.split(sep='/')
            day.append(line[1])
            month.append(line[0])
            year.append(line[2])
        if count == column_to_extract:
            if line[0] == "$":
                line = line.lstrip('$')
            data.append(line)
        if count == max_column:
            count = 0
        else:
            count += 1
    result = pd.DataFrame(list(zip(year, month, day, data)), columns=['Year', 'Month', 'Day', extract_column_name])
    result.to_csv(path + '.csv')
    file.close()
