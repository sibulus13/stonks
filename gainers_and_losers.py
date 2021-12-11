# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import tkinter as tk
from tkinter import ttk
import csv
import pandas as pd
import os
import datetime
import holidays
# %%
# returns the top {percent} of all top % entries from {i} category
def get_frequent(category, index, percent):
    tsxgainers = list(df[category].iloc[-index:])
    listings = []
    for i in tsxgainers:
        i = i[1:-1]
        i = i.replace('\'', '')
        i = i.replace('[', '')
        lists = i.split('], ')
        lists.pop(0)
        for j in lists:
            entries = j.split(', ')
            # symbol, company name
            listings.append((entries[0], entries[1]))
    gainers = dict.fromkeys(set(listings), 0)
    for i in listings:
        gainers[i]+=1
    gainers = dict(sorted(gainers.items(), key=lambda item:item[1], reverse = True))
    gainers = list(gainers.items())
    rt = ''
    rt2 = []
    # save stock if its frequency is at least % of the top frequency, and if the top frequency at least occurred once
    for i in gainers:
        if i[1] > gainers[0][1]*percent and i[1] > 1:
            # print(i)
            rt += str(i) + '\n'
            rt2.append(i)
    return rt, rt2
# %%
# adds daily top losers/gainers to {fname}
if __name__ == "__main__":
    folder = r"Z:\repo\Stonks\stonks"
    os.chdir(folder)

    path = r"Z:\repo\Stonks\stonks\stonkStatistics.csv"

    data = []
    with open(path, mode = 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data.append(row)
    headers = data.pop(0)
    df = pd.DataFrame(data, columns = headers)
    # df = pd.DataFrame(data)
    # print(headers)
    weekno = datetime.datetime.today().weekday()

    days = 3
    perc = 0.5
    msg = ''
    weekdays = {0:"monday",1:"tuesday",2:'wednesday',3:'thursday',4:'friday',5:'saturday',6:'sunday'}
    us_holidays = holidays.US()
    can_holidays = holidays.CA()

    if weekno<5:
        todays = []
        relevant_headers = headers[2:5]
        # print(relevant_headers)
        for category in relevant_headers:
            msg += '__________________'+category+'__________________ \n'
            rt, rt2 = get_frequent(category, days, perc)
            msg += rt + '\n'
            if len(rt2) != 0:

                for j in rt2:
                    today = datetime.date.today()
                    isholidayUS = us_holidays.get(today) or 'None'
                    isholidayCAN = can_holidays.get(today) or 'None'
                    todays.append([today, weekdays[weekno], isholidayUS, isholidayCAN,category, j[0][0], j[0][1], perc, days, j[1], ''])
        fname = 'extremeStonks.csv'
        csvfile = open(fname, 'a+', newline = '')
        spamwriter = csv.writer(csvfile, delimiter = ',')
        header = ['date', 'day of week', 'is US holiday', 'is CAN holiday', 'category', 'symbol', 'name', 'percent', '# cumulative days', '# count',  '% gain',]
        lines = len(open(fname).readlines())
        if lines == 0:
            print('writing header')
            spamwriter.writerow(header)

        for i in todays:
            spamwriter.writerow(i)
        csvfile.close()