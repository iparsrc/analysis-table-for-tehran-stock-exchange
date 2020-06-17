import csv
import jalali
import datetime
import numpy as np
import pandas as pd
import dateutil.relativedelta


def calcCov(end, start, df): # Calculates covariance.
    df = df[(df["date"] >= start) & (df["date"] <= end)][["return", "return_index"]]
    return np.cov(df["return"], df["return_index"])[0][1]

def calcBeta(end, start, df, cov): # Calculates beta.
    df = df[(df["date"] >= start) & (df["date"] <= end)]["return_index"]
    var = np.var(df)
    return cov / var

def calcSD(end, start, df): # Calculates standard deviation.
    df = df[(df["date"] >= start) & (df["date"] <= end)]["return"]
    return np.std(df)

def calcTotalReturn(end, start, df): # Calculates total return value.
    df = df[(df["date"] >= start) & (df["date"] <= end)]["return"]
    return np.sum(df)

def calcCV(end, start, df, sd, tr): # Calculates CV.
    df = df[(df["date"] >= start) & (df["date"] <= end)]
    row_count, _ = df.shape
    return sd / (tr / row_count)

def datetimeToString(date): # Convertes a date object to integer like datetime.date(2020, 1, 12) ---> 20200112.
    date = str(date)
    return int(date[0:4] + date[5:7] + date[8:])

def controlAll(start=None, end=None): # Runs all functions above for calculating table numbers.
    with open("Beta/inData/stocks_urls.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)

        # All are datetime.date() type.
        today = datetime.date.today()
        last_1_month = datetimeToString(today + dateutil.relativedelta.relativedelta(months=-1))
        last_3_month = datetimeToString(today + dateutil.relativedelta.relativedelta(months=-3))
        last_6_month = datetimeToString(today + dateutil.relativedelta.relativedelta(months=-6))
        last_9_month = datetimeToString(today + dateutil.relativedelta.relativedelta(months=-9))
        last_1_year = datetimeToString(today + dateutil.relativedelta.relativedelta(years=-1))
        last_2_year = datetimeToString(today + dateutil.relativedelta.relativedelta(years=-2))
        last_3_year = datetimeToString(today + dateutil.relativedelta.relativedelta(years=-3))
        today = datetimeToString(today)

        df_out_m1 = pd.DataFrame(columns=['ticker', 'cov', 'beta', 'sd', 'tr', 'cv'])
        df_out_m3 = pd.DataFrame(columns=['ticker', 'cov', 'beta', 'sd', 'tr', 'cv'])
        df_out_m6 = pd.DataFrame(columns=['ticker', 'cov', 'beta', 'sd', 'tr', 'cv'])
        df_out_m9 = pd.DataFrame(columns=['ticker', 'cov', 'beta', 'sd', 'tr', 'cv'])
        df_out_y1 = pd.DataFrame(columns=['ticker', 'cov', 'beta', 'sd', 'tr', 'cv'])
        df_out_y2 = pd.DataFrame(columns=['ticker', 'cov', 'beta', 'sd', 'tr', 'cv'])
        df_out_y3 = pd.DataFrame(columns=['ticker', 'cov', 'beta', 'sd', 'tr', 'cv'])

        i = 0 # This is for counting the for loop below.
        for row in reader: # Looping through stock files.
            ticker = row[0]
            file_url = "Beta/outData/stocks/" + ticker + ".csv"
            df = pd.read_csv(file_url)

            # Calculating covariance of index return values and stock return values.
            cov_1_month = calcCov(today, last_1_month, df)
            cov_3_month = calcCov(today, last_3_month, df)
            cov_6_month = calcCov(today, last_6_month, df)
            cov_9_month = calcCov(today, last_9_month, df)
            cov_1_year = calcCov(today, last_1_year, df)
            cov_2_year = calcCov(today, last_2_year, df)
            cov_3_year = calcCov(today, last_3_year, df)

            # Calculating beta for stocks.
            beta_1_month = calcBeta(today, last_1_month, df, cov_1_month)
            beta_3_month = calcBeta(today, last_3_month, df, cov_3_month)
            beta_6_month = calcBeta(today, last_6_month, df, cov_6_month)
            beta_9_month = calcBeta(today, last_9_month, df, cov_9_month)
            beta_1_year = calcBeta(today, last_1_year, df, cov_1_year)
            beta_2_year = calcBeta(today, last_2_year, df, cov_2_year)
            beta_3_year = calcBeta(today, last_3_year, df, cov_3_year)

            # Calculating standard deviation for stocks.
            sd_1_month = calcSD(today, last_1_month, df)
            sd_3_month = calcSD(today, last_3_month, df)
            sd_6_month = calcSD(today, last_6_month, df)
            sd_9_month = calcSD(today, last_9_month, df)
            sd_1_year = calcSD(today, last_1_year, df)
            sd_2_year = calcSD(today, last_2_year, df)
            sd_3_year = calcSD(today, last_3_year, df)

            # Calculating total return value for stocks.
            tr_1_month = calcTotalReturn(today, last_1_month, df)
            tr_3_month = calcTotalReturn(today, last_3_month, df)
            tr_6_month = calcTotalReturn(today, last_6_month, df)
            tr_9_month = calcTotalReturn(today, last_9_month, df)
            tr_1_year = calcTotalReturn(today, last_1_year, df)
            tr_2_year = calcTotalReturn(today, last_2_year, df)
            tr_3_year = calcTotalReturn(today, last_3_year, df)

            # Calculating CV for stocks.
            cv_1_month = calcCV(today, last_1_month, df, sd_1_month, tr_1_month)
            cv_3_month = calcCV(today, last_3_month, df, sd_3_month, tr_3_month)
            cv_6_month = calcCV(today, last_6_month, df, sd_6_month, tr_6_month)
            cv_9_month = calcCV(today, last_9_month, df, sd_9_month, tr_9_month)
            cv_1_year = calcCV(today, last_1_year, df, sd_1_year, tr_1_year)
            cv_2_year = calcCV(today, last_2_year, df, sd_2_year, tr_2_year)
            cv_3_year = calcCV(today, last_3_year, df, sd_3_year, tr_3_year)

            df_out_m1.loc[i] = [ticker, cov_1_month, beta_1_month, sd_1_month, tr_1_month, cv_1_month]
            df_out_m3.loc[i] = [ticker, cov_3_month, beta_3_month, sd_3_month, tr_3_month, cv_3_month]
            df_out_m6.loc[i] = [ticker, cov_6_month, beta_6_month, sd_6_month, tr_6_month, cv_6_month]
            df_out_m9.loc[i] = [ticker, cov_9_month, beta_9_month, sd_9_month, tr_9_month, cv_9_month]
            df_out_y1.loc[i] = [ticker, cov_1_year, beta_1_year, sd_1_year, tr_1_year, cv_1_year]
            df_out_y2.loc[i] = [ticker, cov_2_year, beta_2_year, sd_2_year, tr_2_year, cv_2_year]
            df_out_y3.loc[i] = [ticker, cov_3_year, beta_3_year, sd_3_year, tr_3_year, cv_3_year]
            i += 1

        df_out_m1.to_csv("Beta/outData/m1.csv", index=False, encoding='utf-8-sig')
        df_out_m3.to_csv("Beta/outData/m3.csv", index=False, encoding='utf-8-sig')
        df_out_m6.to_csv("Beta/outData/m6.csv", index=False, encoding='utf-8-sig')
        df_out_m9.to_csv("Beta/outData/m9.csv", index=False, encoding='utf-8-sig')
        df_out_y1.to_csv("Beta/outData/y1.csv", index=False, encoding='utf-8-sig')
        df_out_y2.to_csv("Beta/outData/y2.csv", index=False, encoding='utf-8-sig')
        df_out_y3.to_csv("Beta/outData/y3.csv", index=False, encoding='utf-8-sig')