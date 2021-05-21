from stonkstatistics import *
import time
from selenium import webdriver
from googlesearch import search

folder = r"Z:\sibroot\repo\personal\stonks"
os.chdir(folder)
fname = 'extremeStonks.csv'


def get_change(name):
    print(name)
    # hacky way of getting over http access error?
    # while True:
    #     try:
    #         results = search('yahoo finance '+name+' TSX')
    #         url = list(results)[0]
    #     except Exception as e:
    #         print(e)
    #         time.sleep(1000)
    #         print('continuing... waiting 16min')
    #         continue
    #     break
    url = 'https://ca.finance.yahoo.com/quote/'+name+'.TO'
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.findAll('div', class_ = 'D(ib) Mend(20px)') #, class_ = 'kno-fv' 
    try:
        _, result = results[0].text.split('(')
        result, _ = result.split(')')

    except Exception as e:
        # result = 'unfound'
        try:
            print(e, 'trying google search instead')
            results = search('yahoo finance '+name+' TSX')
            url = list(results)[0]
            print(url)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.findAll('div', class_ = 'D(ib) Mend(20px)') #, class_ = 'kno-fv'
            _, result = results[0].text.split('(')
            result, _ = result.split(')')
        except Exception as e:
            print(e, 'no results found')
            result = 0

    print(result)
    return result

if __name__ == '__main__':
    data = []
    with open(fname, newline = '') as csvfile:
        spamreader = csv.reader(csvfile, delimiter = ',')
        for i in spamreader:
            data.append(i)

    for stock in data: #scrape % change per stock
        replace = False
        for col in range(len(stock)):
            if len(stock[col]) == 0:
                change = get_change(stock[2])
                stock[col] = change
                replace = True
                break
        if replace == False: 
            stock.append(get_change(stock[2]))
    
    for i in data:
        print(i)

    with open(fname, 'w', newline = '') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter = ',')
        spamwriter.writerows(data)