import pandas

def extract_interestratesbonds():
    rates_old = pandas.read_csv('./data/InterestRatesBonds/yield-curve-rates-1990-2021.csv')
    rates_2022 = pandas.read_csv('./data/InterestRatesBonds/daily-treasury-rates_2022.csv')
    rates_2023 = pandas.read_csv('./data/InterestRatesBonds/daily-treasury-rates_2023.csv')
    df = pandas.concat([rates_2023, rates_2022, rates_old])
    df = df.loc[:, ["Date", "2 Yr", "20 Yr"]]
    df["Date"] = df["Date"].apply(lambda x: x[:6] + "20" + x[6:] if (len(x) == 8 and int(x[6:]) < 30) else x)
    df["Date"] = df["Date"].apply(lambda x: x[:5] + "20" + x[5:] if (len(x) == 7 and int(x[5:]) < 30) else x)
    df["Date"] = df["Date"].apply(lambda x: x[:4] + "20" + x[4:] if (len(x) == 6 and int(x[4:]) < 30) else x)
    df[["Month", "Day", "Year"]] = df["Date"].str.split('/', n=2, expand=True)
    df.drop(df[df["Year"].astype(int) < 100].index, inplace=True)
    df.drop(columns="Date", inplace=True)
    df["Day"] = df["Day"].apply(lambda x: x[1] if x[0] == "0" else x)
    df["Month"] = df["Month"].apply(lambda x: x[1] if x[0] == "0" else x)
    df.to_csv('./data/InterestRatesBonds/InterestRatesBonds.csv')