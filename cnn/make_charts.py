from make_prediction import make_prediction

import numpy as np
import pandas as pd
import holidays, datetime
import matplotlib.pyplot as plt

def make_charts():
    data = np.load('./cnn/data/data_sliced.npy')
    to_predict = np.load('./cnn/data/topredict.npy')

    res = make_prediction()
    data_arr = np.zeros((190, 23))
    data_arr[100:, 3:] = res
    i=3
    for val in to_predict:
        data_arr[:100, i] = data[-1, -100:, val]
        i+=1
    for i in range(1, 4):
        data_arr[:100, i-1] = data[-1, -100:, i] #0 year 1 month 2 day

    day = datetime.date.today()
    for i in range(100, 190):
        day = day + datetime.timedelta(days=1)
        while day.weekday in holidays.WEEKEND or day in holidays.US():
            day = day + datetime.timedelta(days=1)
        data_arr[i, 0] = day.year    
        data_arr[i, 1] = day.month
        data_arr[i, 2] = day.day

    df = pd.DataFrame(data=data_arr, columns=['year', 'month', 'day', 'MSFT_Open', 'MSFT_High', 'MSFT_Low', 'MSFT_Close', 'NVDA_Open', 'NVDA_High', 'NVDA_Low', 'NVDA_Close', 'AAPL_Open', 'AAPL_High', 'AAPL_Low', 'AAPL_Close', 'AMZN_Open', 'AMZN_High', 'AMZN_Low', 'AMZN_Close', 'AMD_Open', 'AMD_High', 'AMD_Low', 'AMD_Close'])
    df['date'] = pd.to_datetime(df[['day', 'month', 'year']], format='%d%m%Y')

    companies = ["MSFT", "NVDA", "AAPL", "AMZN", "AMD"]
    width = 0.8
    width2 = .1
    col1 = 'green'
    col2 = 'red'

    for company in companies:
        plt.figure()
    
        up = df[df[company + "_Close"] >= df[company + "_Open"]]
        down = df[df[company + "_Close"] < df[company + "_Open"]]

        plt.bar(up.date,up[company + "_Close"] - up[company + "_Open"],width,bottom=up[company + "_Open"],color=col1)
        plt.bar(up.date,up[company + "_High"] - up[company + "_Close"],width2, bottom=up[company + "_Close"] ,color=col1)
        plt.bar(up.date,up[company + "_Low"] - up[company + "_Open"],width2,bottom=up[company + "_Open"],color=col1)

        plt.bar(down.date,down[company + "_Close"]-down[company + "_Open"],width,bottom=down[company + "_Open"],color=col2)
        plt.bar(down.date,down[company + "_High"]-down[company + "_Open"],width2,bottom=down[company + "_Open"],color=col2)
        plt.bar(down.date,down[company + "_Low"]-down[company + "_Close"],width2,bottom=down[company + "_Close"],color=col2)

        plt.xticks(rotation=30, ha='right')

        plt.savefig("./cnn/charts/" + company + ".png", dpi=250)