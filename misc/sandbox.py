from gainers_and_losers_records import *
from newspaper import Article

def search_results(string):
    results = search(string)
    # for i in results:
        # print(i) 
    return results

# attempting to create a semantic article analyzer
text = 'Ballard Power Systems Inc. Recent News'
# results = list(search_results(text))
# page = requests.get(text)
# soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.text)
# results = soup.findAll('div', class_ = 'D(ib) Mend(20px)') #, class_ = 'kno-fv' 
# result = results[0]
# article = Article(result)
# article.download()
# article.parse()
# print(article.text)