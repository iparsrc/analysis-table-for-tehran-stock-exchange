import pandas as pd

def fix():
    file_url = "Beta/inData/index/index.csv"
    df = pd.read_csv(file_url)
    df.drop_duplicates(subset="date", keep="last", inplace=True)
    df.to_csv(file_url, index=False) # 20180805.