import csv
import jalali
import os.path
import numpy as np
import pandas as pd


def checkFiles(): # Checks existense of all files and if any file don't exist it will create that file.
    try:
        with open("Beta/inData/stocks_urls.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                file_url = "Beta/inData/stocks/" + row[0] + ".csv"
                if not os.path.isfile(file_url): # Checks for file existense.
                    f = open(file_url, "w") # Create file.
                    f.close() # Close created file.
        return True # Return True if checking was successful.
    except:
        return False # Return False if checking was not successful.

def updateFiles(): # Updates csv files.
    isDone = checkFiles() # First checking for file existence.
    if isDone: # If file existence was successful.
        try:
            with open("Beta/inData/stocks_urls.csv", "r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    file_url = "Beta/inData/stocks/" + row[0] + ".csv"
                    download_link = "http://www.tsetmc.com/tsev2/data/Export-txt.aspx?t=i&a=1&b=0&i={}".format(row[1])
                    df = pd.read_csv(download_link) # Downloading data from download_link. (tsetmc.com)
                    df = df[["<DTYYYYMMDD>", "<CLOSE>"]] # Filtering data to two needed columns.
                    df["<RETURN>"] = np.nan
                    df["<RETURN_INDEX>"] = np.nan
                    df.to_csv(file_url, index=False, header=["date", "close", "return", "return_index"], encoding="utf-8-sig") # Writing dataframe to related csv file.
            return True # Returns true if the process did well.
        except:
            return False # Returns false if the process failed.
    return False # Returns false if the cheking process failes.

def calcReturn(): # Calculate profit return for all stock csv files. and rewrites them.
    with open("Beta/inData/stocks_urls.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader: # Loops through all files.
            file_url = "Beta/inData/stocks/" + row[0] + ".csv"
            df = pd.read_csv(file_url) # Reades csv fils.
            for tuple_row in df.itertuples(): # Loops through csv file.
                try:
                    index = tuple_row.Index
                    p2 = tuple_row.close
                    p1 = df.iloc[index + 1, 1]
                    return_value = ((p2 - p1) / p1) * 100 # Calculates the return value.
                    df.iloc[index, 2] = return_value # Modifies the dataframe.
                    # Note that at the end an exception will raise because there will be no next row.
                except:
                    df.iloc[index, 2] = 0.0
                    df.to_csv(file_url, index=False, header=["date", "close", "return", "return_index"], encoding="utf-8") # Writes new data frame to csv file.

    # TODO: it is note actually: Csv file must have date, value, return headers.
    df = pd.read_csv("Beta/inData/index/index.csv") # Reading index csv file.
    df["return"] = np.nan # Creating new column and assigning the to numpy nan.
    for tuple_row in df.itertuples(): # Looping through dataFrame.
        try:
            index = tuple_row.Index
            p2 = tuple_row.value
            p1 = df.iloc[index + 1, 1]
            return_value = ((p2 - p1) / p1) * 100 # Caculating return value.
            df.iloc[index, 2] = return_value # Writing reutrn value to dataFrame.
        except:
            df.iloc[index, 2] = 0.0 # Writing 0 to last row in dataFrame.
            df.to_csv("Beta/inData/index/index.csv", index=False, header=["date", "value", "return"], encoding="utf-8") # Writing dataFrame to csv file.

def createOutData():
    with open("Beta/inData/stocks_urls.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        df_index = pd.read_csv("Beta/inData/index/index.csv") # Making dataFrame from index's csv file.
        df_index.set_index('date', inplace=True)
        drop_list = list() # This is dropping list for drop in the end of indexing proccess.
        for row in reader: # Loop through csv stock files.
            file_url = "Beta/inData/stocks/" + row[0] + ".csv" # Creating stock's csv file url.
            df_stock = pd.read_csv(file_url) # Making dataFrame from stock's csv file.
            row_count, _ = df_stock.shape
            for row_stock in df_stock.itertuples(): # Looping through stock's dataFrame.
                gregorian = str(row_stock.date)
                g_year = gregorian[0:4]
                g_month = gregorian[4:6]
                g_day = gregorian[6:]
                j_year, j_month, j_day = jalali.Gregorian(g_year + ',' + g_month + ',' + g_day).persian_tuple()
                if j_month < 10:
                    j_month = "0" + str(j_month)
                if j_day < 10:
                    j_day = "0" + str(j_day)
                j_date = int(str(j_year) + str(j_month) + str(j_day)) # Jalali date is for searching from df_index.
                try:
                    index_return = df_index.loc[j_date, 'return'] # Trying to get index_return from df_index based on jalali date.
                    df_stock.iloc[row_stock.Index, 3] = index_return # Writing index_return value to df_stock where needed.
                    if row_stock.Index+1 == row_count:
                        raise Exception("For loop finished before index_reuturn ended.")
                except: # Getting exception when df_index.loc[j_date, 'return'] throws IndexError.
                    # TODO: Some stock data's are till 139500101 so the if never executes.
                    # TODO: Then drop list contains the indexes for last stocks miss for drop.
                    if (j_date < 13950101) or (row_stock.Index+1 == row_count):
                        df_stock = df_stock.iloc[:row_stock.Index] # Index now is less than date so we don't need that in dataframe.
                        for item in drop_list:
                            df_stock.drop(item, axis=0, inplace=True)
                        drop_list.clear()
                        break
                    df_stock.iloc[row_stock.Index, 3] = "------------"
                    drop_list.append(row_stock.Index)
                    '''
                    df_stock.drop(row_stock.Index, inplace=True)
                    The problem with drop:
                        Suppose, the row that we want to delete is called 'D' has the index of 10 
                        and the next row is called 'N' and has the index of 11.
                        If we call the drop method for 'D', it drops the row and sets the index of 'N'
                        to 10.
                        Now, the problem is that the next loop is going to start from 11 because it was in 10.
                        So, the row 'N' is not going to be proccessed.
                    '''
            df_stock.to_csv("Beta/outData/stocks/" + row[0] + ".csv", index=False, encoding="utf-8-sig") # Writes new dataFrame to outData stock csv file.





