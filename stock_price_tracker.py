import requests
from bs4 import BeautifulSoup as bs
from stock_class import stock_info
import tkinter as tk

# function loads webpage for scraping if ticker can be found
def load_webpage(symbol):
    # uses symbol input to request a yahoo page of ticker symbol
    r = requests.get('https://finance.yahoo.com/quote/' + symbol + '?p=' + symbol + '&.tsrc=fin-srch')
    webpage=bs(r.content, features="html5lib")

    # this section will look for the first body element
    body = webpage.find('body')
    # will store boolean depending on in the body element has the string under
    is_there_404 = "Our engineers are working quickly to resolve the issue." in body.get_text()
    if is_there_404:
        return False
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

# function will check status of webpage and return a formatted string if available
def main(symbol):
    webpage = load_webpage(symbol)
    # str will be return based on if an actual webpage was returned
    if not webpage:
        final_str = 'Ticker Symbol Not Found'
    else:
        # gets all needed information from webpage and stores it into a stock class instance
        company_name, close_price, all_stats = find_stock_info(webpage)
        # uses stock_class.py to create a stock class and gets all info and returns it into a variable
        company = stock_info(close_price, all_stats[0],all_stats[6],all_stats[4])
        close_price = company.get_close()
        previous_close = company.get_previous_close()
        market_cap = company.get_market_cap()
        volume = company.get_volume()

        # formats each description into a str to pass onto the GUI label
        final_str = "%s\nClose: %s\nPrevious Close: %s\nMarket Cap: %s\nVolume: %s" % (company_name,
                                                                                    close_price,
                                                                                    previous_close,
                                                                                    market_cap,
                                                                                    volume)
    return final_str

# function gets symbol from GUI Entry and sends it over to main part of program
# to get stock description
def search_symbol():
    symbol = ticker_entry.get().strip().upper()
    final_desc = main(symbol)
    stock_text["text"] = f'{final_desc}'


# activate GUI window
window = tk.Tk()

# set window title
window.title('Stock Info')

# create a frame to hold ticker entry and button
ticker_frame = tk.Frame(master=window, relief=tk.FLAT, borderwidth=3)
ticker_frame.pack()

# creates the label, entry box, and search button for the ticker symbol
ticker_label = tk.Label(master=ticker_frame, text='Enter ticker symbol: ', font=('TkDefaultFont',16))
ticker_label.grid(row=0, column=0, sticky='e')
ticker_entry = tk.Entry(master=ticker_frame, width=50)
ticker_entry.grid(row=0, column=1)
search_button = tk.Button(master=ticker_frame, text='Search', command=search_symbol)
search_button.grid(row=0, column=2)

# creates a second frame for the stock info after pressing the search button
info_frame = tk.Frame(master=window, relief=tk.FLAT, )
info_frame.pack()

# creates text box that will show the stock info
stock_text = tk.Label(master=info_frame, text='No Stock Information Yet', font=('TkDefaultFont',18))
stock_text.grid(row=0, column=0)


# starts application
window.mainloop()