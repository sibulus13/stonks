import datetime
import csv
import re
import requests
from bs4 import BeautifulSoup
import re
import os

# scrapes charted info of url based on market and type
def getStonkData(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('div', class_ = "genTable")
    info = results.find_all('td', text=True)
    stonks = [['symbol','company name','last','change','%change','volume']]
    stonk = []
    counter = 0
    for i in info:
        stonk.append(i.text)
        counter+=1
        if counter == 6:
            stonks.append(stonk)
            stonk = []
            counter = 0
    return stonks



if __name__ == '__main__':
    folder = r"Z:\repo\Stonks\stonks"
    os.chdir(folder)
    today = datetime.date.today()
    day = datetime.date.weekday(today)
    weekdays = {0:"Monday",1:"Tuesday",2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}
    base = "https://www.investcom.com/"
    markets ={'TSX':'toronto','TSX Venture':'cdnx','NEX Board':'nex','CSE':'cse','US AMEX':'amex','US NASDAQ':'nasdaq','US NYSE':'nyse','US OTC':'bulletin'}
    types = {'Most Active':'mv','Top % Gainers':'mpg','Top % Losers':'mpl'}
    header = ['date','day']
    data = [today, weekdays[day]]
    if day < 5:
        fname = 'stonkStatistics.csv'
        csvfile = open(fname,'a+', newline = '')
        spamreader = csv.reader(csvfile, delimiter = ',')
        spamwriter = csv.writer(csvfile, delimiter= ',')
        r = len(list(spamreader))
        for market in markets:
            for t in types:
                header.append(market+' '+t)
        
        lines = len(open(fname).readlines())
        # print(lines)
        if lines == 0:
            print('writing header')
            spamwriter.writerow(header)

        for market in markets:
            for t in types:
                try:
                    loc = 'page/' if re.search('US', market) == None else 'us/'
                    url = base+loc+types[t]+markets[market]+'.htm'
                    print([market, t])
                    # print(url)
                    stonks = getStonkData(url)
                    data.append(stonks)
                except Exception as e:
                    print(e)
                    data.append(e)
        spamwriter.writerow(data)
        csvfile.close()