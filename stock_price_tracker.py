import requests
from bs4 import BeautifulSoup as bs
from stock_class import stock_info


def load_webpage(symbol):
    # uses symbol input to request a yahoo page of ticker symbol
    r = requests.get('https://finance.yahoo.com/quote/' + symbol + '?p=' + symbol + '&.tsrc=fin-srch')
    webpage=bs(r.content, features="html5lib")

    # this section will look for the first body element
    body = webpage.find('body')
    # will store boolean depending on in the body element has the string under
    is_there_404 = "Our engineers are working quickly to resolve the issue." in body.get_text()
    if is_there_404:
        print('Ticker symbol not found. Please enter a valid ticker symbol.')
    else:
        return webpage

# function will scrape for the stock's main statistics
def find_stock_info(webpage):

    # returns the company name element
    company_name = webpage.find('h1', attrs={'class':'D(ib) Fz(18px)'})

    # scrapes the heading of the page and extracts the most recent close of the stock
    stock_heading = webpage.find('div', attrs={'data-reactid':'47'})
    stock_close = stock_heading.find('span',attrs={'class':'Trsdu(0.3s)'})

    # Yahoo's stock stats are separated into two tables, so I scraped them as separate entities
    left_table = webpage.find('table', attrs={'data-reactid':'91'})
    right_table = webpage.find('table', attrs={'data-reactid':'132'})
    left_table = left_table.find_all('span', attrs={'class':'Trsdu(0.3s)'})# used to get further into table element
    right_table = right_table.find_all('span', attrs={'class':'Trsdu(0.3s)'})

    # adds all text from both tables into a list
    all_stats = []
    for stat in left_table:
         all_stats.append(stat.get_text())
    for stat in right_table:
        all_stats.append(stat.get_text())
    
    return company_name.get_text(), stock_close.get_text(), all_stats

def main():
    # asks user for ticker symbol
    symbol = input('Enter ticker symbol: ').strip().upper()
    print()
    webpage = load_webpage(symbol)
    company_name, close_price, all_stats = find_stock_info(webpage)

    # uses stock_class.py to create a stock class and gets all info and returns it into a variable
    company = stock_info(close_price, all_stats[0],all_stats[6],all_stats[4])
    close_price = company.get_close()
    previous_close = company.get_previous_close()
    market_cap = company.get_market_cap()
    volume = company.get_volume()

    # prints the stock's stats
    print('Company: ' + company_name)
    print('--------------------------------------')
    print('Close Price: ' + close_price + '\n' +
          'Previous Close: ' + previous_close + '\n' +
          'Market Cap: ' + market_cap + '\n' +
          'Volume: ' + volume)
    print()

main()

