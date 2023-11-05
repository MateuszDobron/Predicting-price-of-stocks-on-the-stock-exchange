import yfinance as yf
import time
import pandas as pd
import numpy as np

# modify to get expected dataset
start_year = "2005" # recommended min start_year is 2005, because since then we have financial data
start_month = "01"  # for x month 0x
start_day = "1"
interval = "1d"  # 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo so far choose day interval

# assumed possible companies apple microsoft amazon alphabet nvidia
# just modify the set
# companies = {"apple", "microsoft", "amazon", "alphabet", "nvidia"}

# Open, High, Low, Close are always present
# Change to true if it should be present false otherwise
volume_contain = True

# roe, roa, eps for chosen companies
financial_data = True

# if all present order may be stock price, financials, ... , macro
sort = True

# do not  modify things below
companies_tickers_list = ["MSFT", "NVDA", "AAPL", "AMZN", "GOOG"]
# for company in companies:
#     if company == "apple":
#         companies_tickers_list.append("AAPL")
#     if company == "microsoft":
#         companies_tickers_list.append("MSFT")
#     if company == "amazon":
#         companies_tickers_list.append("AMZN")
#     if company == "alphabet":
#         companies_tickers_list.append("GOOG")
#     if company == "nvidia":
#         companies_tickers_list.append("NVDA")

print(companies_tickers_list)
data_temp = yf.download(tickers=companies_tickers_list, start=start_year + "-" + start_month + "-" + start_day,
                   interval=interval, group_by="ticker")
print(data_temp.columns)

data = {'Year': data_temp.index.year.tolist(),
        'Month': data_temp.index.month.tolist(),
        'Day': data_temp.index.day.tolist()}
df = pd.DataFrame(data)

if len(companies_tickers_list) > 1:
    for company in companies_tickers_list:
        df[company+"_Open"] = np.round(data_temp[(company, 'Open')], 2).tolist()
        df[company + "_High"] = np.round(data_temp[(company, 'High')], 2).tolist()
        df[company + "_Low"] = np.round(data_temp[(company, 'Low')], 2).tolist()
        df[company + "_Close"] = np.round(data_temp[(company, 'Close')], 2).tolist()
        if volume_contain:
            df[company + "_Volume"] = data_temp[(company, 'Volume')].tolist()
else:
    df[companies_tickers_list[0] + "_Open"] = np.round(data_temp['Open'], 2).tolist()
    df[companies_tickers_list[0] + "_High"] = np.round(data_temp['High'], 2).tolist()
    df[companies_tickers_list[0] + "_Low"] = np.round(data_temp['Low'], 2).tolist()
    df[companies_tickers_list[0] + "_Close"] = np.round(data_temp['Close'], 2).tolist()
    if volume_contain:
        df[companies_tickers_list[0] + "_Volume"] = data_temp['Volume'].tolist()

df["Date"] = df["Year"].astype(str) + '-' + df["Month"].astype(str) + '-' + df["Day"].astype(str)
df["Date"] = pd.to_datetime(df["Date"], format='%Y-%m-%d')

financial_indicators = ["ROE", "ROA", "EPS"]
if financial_data:
    for company_ticker in companies_tickers_list:
        for indicator in financial_indicators:
            data = pd.read_csv('./scraping/data/' + company_ticker + '/' + company_ticker + '_' + indicator + '.csv')
            data["Date"] = data["Year"].astype(str) + '-' + data["Month"].astype(str) + '-' + data["Day"].astype(str)
            data["Date"] = pd.to_datetime(data["Date"], format='%Y-%m-%d')
            list_of_values = list()
            for index, row in df.iterrows():
                x = data.loc[data["Date"] < row["Date"], indicator].head(1)
                if type(x) == pd.Series.empty:
                    raise ValueError("no fanancial data available for such early date")
                list_of_values.append(x.item())
            df[company_ticker + '_' + indicator] = list_of_values
        df[company_ticker + '_ROE'] = df[company_ticker + '_ROE'].str.replace('%', '')
        df[company_ticker + '_ROA'] = df[company_ticker + '_ROA'].str.replace('%', '')

# bonds interest
data = pd.read_csv('./scraping/data/InterestRatesBonds/InterestRatesBonds.csv')
data["Date"] = data["Year"].astype(str) + '-' + data["Month"].astype(str) + '-' + data["Day"].astype(str)
data["Date"] = pd.to_datetime(data["Date"], format='%Y-%m-%d')
list_of_values_2 = list()
list_of_values_20 = list()
for index, row in df.iterrows():
    x = data.loc[data["Date"] < row["Date"], ["2 Yr", "20 Yr"]].head(1)
    if type(x) == pd.Series.empty:
        raise ValueError("no bond data available for such early date")
    list_of_values_2.append(x["2 Yr"].item())
    list_of_values_20.append(x["20 Yr"].item())
    
df["2 Yr"] = list_of_values_2
df["20 Yr"] = list_of_values_20

#CPI
data = pd.read_csv('./scraping/data/CPI/CPI.csv')
data["Date"] = data["Year"].astype(str) + '-' + data["Month"].astype(str)
data["Date"] = pd.to_datetime(data["Date"], format='%Y-%m')
list_of_values = list()
for index, row in df.iterrows():
    x = data.loc[(data["Date"] + pd.DateOffset(months=2)) < row["Date"], "CPI"].head(1) # cpi info is later than beginning of the next month
    if type(x) == pd.Series.empty:
        raise ValueError("no bond data available for such early date")
    list_of_values.append(x.item())

df["CPI"] = list_of_values

#money supply
data = pd.read_csv('./scraping/data/MoneySupply/MoneySupply.csv')
data["Date"] = data["Year"].astype(str) + '-' + data["Month"].astype(str)
data["Date"] = pd.to_datetime(data["Date"], format='%Y-%m')
list_of_values_M1 = list()
list_of_values_M2 = list()
for index, row in df.iterrows():
    x = data.loc[(data["Date"] + pd.DateOffset(months=2)) < row["Date"], ["M1", "M2"]].tail(1) # moneysupply info is later than beginning of the next month
    if type(x) == pd.Series.empty:
        raise ValueError("no bond data available for such early date")
    list_of_values_M1.append(x["M1"].item())
    list_of_values_M2.append(x["M2"].item())

df["M1"] = list_of_values_M1
df["M2"] = list_of_values_M2

if sorted: 
    final_order = list()
    final_order.append('Year')
    final_order.append('Month')
    final_order.append('Day')
    for company_ticker in companies_tickers_list:
        final_order.append(company_ticker + '_Open')
        final_order.append(company_ticker + '_High')
        final_order.append(company_ticker + '_Low')
        final_order.append(company_ticker + '_Close')
        final_order.append(company_ticker + '_Volume')
        for indicator in financial_indicators:
            final_order.append(company_ticker + '_' + indicator)
    final_order.append('2 Yr')
    final_order.append('20 Yr')
    final_order.append('CPI')
    final_order.append('M1')
    final_order.append('M2')
    df = df[final_order]

for column in df.columns:
    df[column] = df[column].astype(str)
    df[column] = df[column].str.replace("$", "")
    df[column] = df[column].str.replace(",", ".")
    df[column] = df[column].astype(float)

df.to_csv('./dataset/dataset.csv')
