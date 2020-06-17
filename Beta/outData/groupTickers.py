import csv
import pandas as pd
import numpy as np


def groupData(timeDelta):
    df_stock_urls = pd.read_csv("Beta/inData/stocks_urls.csv", names=["ticker", "code", "group_name"])
    df_stock_urls.set_index("ticker", inplace=True)
    output_file_url = "Beta/outData/" + timeDelta + ".csv"
    df = pd.read_csv(output_file_url)
    df["group_name"] = np.nan
    df.set_index("ticker", inplace=True)

    for row in df.itertuples():
        ticker = row.Index
        group_name = df_stock_urls.loc[ticker, "group_name"]
        df.loc[ticker, "group_name"] = group_name
    df.to_csv(output_file_url)

def controlGrouping():
    groupData("m1")
    groupData("m3")
    groupData("m6")
    groupData("m9")
    groupData("y1")
    groupData("y2")
    groupData("y3")