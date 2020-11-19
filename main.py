import json
import datetime as dt

import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import requests as req
import bs4 as bs

PRICES_URL = 'https://www.agron.com.br/widgets/cotacao_interna.php'

def get_prices():
    res = req.get(PRICES_URL)
    soup = bs.BeautifulSoup(res.text, features='lxml')
    table = soup.find('body')
    # table = soup.find('table', {"id": "constituents"})
    # tickers = []
    # for row in table.findAll('tr')[1:]:
    #     ticker = row.find('td').text
    #     # Tickers can come with the new line character and we don't want that.
    #     ticker = ticker.replace('\n','')
    #     # Some stock tickers contain a dot instead of a hyphen. Ex: in Wikipedia
    #     # Brown-Forman Corp is listed BF.B, but in Yahoo it's listed BF-B.
    #     if "." in ticker:
    #         ticker = ticker.replace('.','-')
    #         print('ticker replaced to', ticker)
    #     tickers.append(ticker)

    # with open('../data/sp500_tickers.pickle', 'wb') as f:
    #     pickle.dump(tickers, f)
    #
    # print('reloaded S&P 500 tickers')
    return table

# with open('test.txt', 'w+') as f:
#     text = get_prices()
#     f.write(text)
#     print('done')


'''corn futures'''

stock_ticker = 'ZC=F'  # corn future dec 2020
stock_ticker = 'ZCH21.CBT'  # corn future mar 2021

'''
Gets stock data from Yahoo and saves as a csv
'''

style.use('ggplot')

# keep in mind that your stock might not have been traded in the entire period
start = dt.datetime(2020, 1, 1)
end = dt.datetime(2020,12,31)

df = web.DataReader(stock_ticker, 'yahoo', start, end)
df.to_csv(f'./csv/{stock_ticker}.csv')

# we use parse_dates and index_col so date is an index (and it's column 0)
df  = pd.read_csv(f'./csv/{stock_ticker}.csv', parse_dates=True, index_col=0)
print(df.head())

fig, ax = plt.subplots()
ax.set_ylabel('USD (U$)')

title = f'(CBOT: Corn Futures Mar 2021) '
df['Adj Close'].plot(title=title, ax=ax)
plt.show()
