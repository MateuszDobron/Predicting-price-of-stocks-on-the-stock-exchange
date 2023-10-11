import yfinance as yf
import time
import pandas as pd

# modify to get expected dataset
start_year = "2020"
start_month = "01"  # for x month 0x
start_day = "1"
interval = "1wk"  # 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo

# assumed possible companies apple microsoft amazon alphabet nvidia
# just modify the set
companies = {"apple"}

# Open, High, Low, Close are always present
# Change to true if it should be present false otherwise
volume_contain = True


# do not  modify things below
companies_tickers_list = []
for company in companies:
    if company == "apple":
        companies_tickers_list.append("AAPL")
    if company == "microsoft":
        companies_tickers_list.append("MSFT")

print(companies_tickers_list)
data_temp = yf.download(tickers=companies_tickers_list, start=start_year + "-" + start_month + "-" + start_day,
                   interval=interval, group_by="ticker")
print(data_temp.columns)
# print(data_temp[('MSFT', 'Open')].tolist())
data = {'Year': data_temp.index.year.tolist(),
        'Month': data_temp.index.month.tolist(),
        'Day': data_temp.index.day.tolist()}
df = pd.DataFrame(data)

if len(companies_tickers_list) > 1:
    for company in companies_tickers_list:
        df[company+"_Open"] = data_temp[(company, 'Open')].tolist()
        df[company + "_High"] = data_temp[(company, 'High')].tolist()
        df[company + "_Low"] = data_temp[(company, 'Low')].tolist()
        df[company + "_Close"] = data_temp[(company, 'Close')].tolist()
        if volume_contain:
            df[company + "_Volume"] = data_temp[(company, 'Volume')].tolist()
else:
    df[companies_tickers_list[0] + "_Open"] = data_temp['Open'].tolist()
    df[companies_tickers_list[0] + "_High"] = data_temp['High'].tolist()
    df[companies_tickers_list[0] + "_Low"] = data_temp['Low'].tolist()
    df[companies_tickers_list[0] + "_Close"] = data_temp['Close'].tolist()
    if volume_contain:
        df[companies_tickers_list[0] + "_Volume"] = data_temp['Volume'].tolist()
print(df)
print(df.columns)
# print(data.columns)
# print(data)
