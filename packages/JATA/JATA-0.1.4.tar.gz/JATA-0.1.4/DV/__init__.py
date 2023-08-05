import subprocess
import sys

import nltk
import numpy as np
import pandas as pd

try:
    import geograpy
except BaseException as e:
    def install(package):
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


    install("geograpy3")
    import geograpy
nltk.download('popular')
chart_width = 550
chart_height = 400
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def clean_df(df):
    def trim_all_columns(df):
        """
        Trim whitespace from ends of each value across all series in dataframe
        """
        trim_strings = lambda x: x.strip() if isinstance(x, str) else x
        return df.applymap(trim_strings)

    df.replace("\n", '', inplace=True)
    df.replace("\t", '', inplace=True)
    df.replace("", np.nan, inplace=True)
    df = trim_all_columns(df)
    return (df)


def clean_dates(dataframe):
    outList = []
    for i in dataframe.itertuples():
        strI = (i.Dates)

        # print(strI)
        if isinstance(strI, int):
            outList.append(strI)
            pass
        else:

            strI = (strI.replace('–', ' ', 10))
            strI = (strI.replace('-', ' ', 10))

            strI = (strI.replace(',', ' ', 10))
            # strI = (strI.replace('–',' ',10))
            # print(strI)
            dates = strI.split()
            cleaned = [int(x) for x in dates if x.isdigit()]
            cleaned = [item for item in cleaned if item >= 1000]

            # print(dates)
            outList.extend(cleaned)
    return outList


def clean_dates_avg(dataframe):
    def Average(lst):
        try:
            return sum(lst) / len(lst)
        except BaseException as E:
            print(E, lst)
            return ''

    outList = []
    for i in dataframe.itertuples():
        strI = (i.Dates)

        # print(strI)
        if isinstance(strI, int):
            outList.append(strI)
            pass
        else:

            strI = (strI.replace('–', ' ', 10))
            strI = (strI.replace('-', ' ', 10))

            strI = (strI.replace(',', ' ', 10))
            # strI = (strI.replace('–',' ',10))
            # print(strI)
            dates = strI.split()
            cleaned = [int(x) for x in dates if x.isdigit()]
            cleaned = [item for item in cleaned if item >= 1000]
            cleaned = Average(cleaned)
            # print(cleaned)
            # print(dates)
            outList.append((cleaned))
    return outList


def make_date_columns(df):
    newList = clean_dates_avg(df)
    df['Avg Date'] = newList


def make_geo_columns(df, original_col):
    df[original_col] = df[original_col].astype(str)
    df['Cities'] = df.apply(lambda row: geograpy.get_place_context(text=row[original_col]).cities, axis=1)
    df["City"] = df["Cities"].str[0]


def clean_langs(df, original_col):
    df[original_col] = df[original_col].astype(str).replace('From the Sub-Series:', ' ')
    df[original_col] = df[original_col].replace('The collection is in ', '')


def clean_locations(df):
    boxList = []
    folderList = []
    for i in df.itertuples():
        loc = i._9
        # print(loc)
        try:

            box = str(loc).split('Box:')[1].split(',')[0]
        except BaseException as e:
            box = ''

        try:

            folder = str(loc).split('Folder:')[1].split('(')[0]
        except BaseException as e:
            folder = ''
        # print(box, folder)
        validation_test = (len(box) + len(folder))
        # print(validation_test)
        if validation_test > 100:
            box, folder = ('', '')
        boxList.append(box)
        folderList.append(folder)

    df['Box'] = boxList
    df['Folder'] = folderList
