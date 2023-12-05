import pandas
import numpy as np

def extract_cpi():
    Dict = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec"
    }
    data = pandas.read_excel('./dataset/data/CPI/SeriesReport.xlsx')
    data.drop(data[data["Year"].astype(int) < 1999].index, inplace=True)
    df = pandas.DataFrame()
    for year in range(2023, 1999, -1):
        for month in range (12, 0, -1):
            if data.loc[data["Year"]==year, Dict[month]].isnull().item():
                continue
            new_record = pandas.DataFrame([{"Year": year, "Month": month, 
                                            "CPI":np.round(((data.loc[data["Year"]==year, Dict[month]].item() - data.loc[data["Year"]==year - 1, Dict[month]].item()) / data.loc[data["Year"]==year - 1, Dict[month]].item())*100, 1)}])
            df = pandas.concat([df, new_record], ignore_index=True)
    df.to_csv('./dataset/data/CPI/CPI.csv')