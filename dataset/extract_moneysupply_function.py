import pandas, os
import numpy as np

def extract_moneysupply():
     if os.path.exists('./dataset/data/MoneySupply/MoneySupply.csv'):
        os.remove('./dataset/data/MoneySupply/MoneySupply.csv')
     file = pandas.read_csv('./dataset/data/MoneySupply/FRB_H6.csv')
     d = {'Year': file.loc[5:,"Series Description"].str[0:4], 'Month': file.loc[5:,"Series Description"].str[5:],
          'M1': file.loc[5:,"M1; Not seasonally adjusted"], 'M2': file.loc[5:,"M2; Not seasonally adjusted"]}
     df = pandas.DataFrame(data=d)
     df["Month"] = df["Month"].apply(lambda x: x[1] if x[0] == '0' else x)
     df = df.reset_index(drop=True)
     print(df)
     df.to_csv('./dataset/data/MoneySupply/MoneySupply.csv')