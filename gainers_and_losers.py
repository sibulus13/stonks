# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%

import tkinter as tk
from tkinter import ttk
import datetime
import csv
import pandas as pd
import os
folder = r"Z:\sibroot\repo\personal\stonks"
os.chdir(folder)

path = r'Z:\sibroot\repo\personal\stonks\stonkStatistics.csv'

data = []
with open(path, mode = 'r') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        data.append(row)
headers = data.pop(0)
df = pd.DataFrame(data, columns = headers)


# %%
# print(df['TSX Top % Gainers'])
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
import datetime
weekno = datetime.datetime.today().weekday()

days = 3
perc = 0.7
msg = ''

if weekno<5:
    todays = []
    for i in ['TSX Top % Gainers', 'TSX Top % Losers']:
        msg += '__________________'+i+'__________________ \n'
        rt, rt2 = get_frequent(i, days, perc)
        msg += rt + '\n'
        if len(rt2) != 0:
            for j in rt2:
                todays.append([datetime.date.today(), i, j[0][0], j[0][1], perc, days, j[1], ''])
            # todays.append([datetime.date.today(), i, rt2[0][0][0], rt2[0][0][1], perc, days, rt2[0][1]])
    # popup = tk.Tk()
    # popup.wm_title('Daily Extreme Stonks')
    # label = ttk.Label(popup, text = msg)
    # label.pack()
    # B1 = ttk.Button(popup, text = 'okay', command = popup.destroy)
    # B1.pack()
    # popup.after(1000000, popup.destroy)
    # popup.mainloop()

fname = 'extremeStonks.csv'
csvfile = open(fname, 'a+', newline = '')
spamwriter = csv.writer(csvfile, delimiter = ',')
for i in todays:
    spamwriter.writerow(i)
csvfile.close()