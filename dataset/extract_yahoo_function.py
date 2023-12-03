import os
import datetime
import pandas as pd

def extract_yahoo(path):
    Dict = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12 
    }
    if os.path.exists(path + '.csv'):
        os.remove(path + '.csv')
    file = open(path + '.txt')
    lines = file.readlines()
    day = []
    month = []
    year = []
    for line in lines:
        if datetime.date.today() > datetime.date(int(line[8:12]), int(Dict[line[0:3]]), int(line[4:6])):
            day.append(line[4:6])
            month.append(Dict[line[0:3]])
            year.append(line[8:12])
    result = pd.DataFrame(list(zip(year, month, day)), columns=['Year', 'Month', 'Day'])
    result.to_csv(path + '.csv')
    file.close()

        