import requests
from bs4 import BeautifulSoup as bs
from stock_class import stock_info
import tkinter as tk

# function loads webpage for scraping if ticker can be found
def load_webpage(symbol):
    # uses symbol input to request a yahoo page of ticker symbol
    r = requests.get('https://finance.yahoo.com/quote/' + symbol).text
    webpage=bs(r, features="html.parser")

    # this section will look for the first body element
    body = webpage.find('body')

    return body

# function will scrape for the stock's main statistics
def find_stock_info(body):
    try:
        # returns the company name element
        stock_name = body.find('h1', attrs={'class':'yf-3a2v0c'}).text

        # scrapes the most recent close of the stock
        stock_close = float(body.find('fin-streamer', attrs={'data-field':'regularMarketPrice'}).find('span').text.strip())

        # scrapes the previous close of the stock
        stock_prev_close = float(body.find('fin-streamer', attrs={'data-field':'regularMarketPreviousClose'}).text.strip())

        # scrapes the volume of the stock
        volume = int(body.find('fin-streamer', attrs={'data-field':'regularMarketVolume'}).text.strip().replace(",",""))

        # scrapes the market cap of the stock
        market_cap = body.find('fin-streamer', attrs={'data-field':'marketCap'}).text

        # create stock object
        stock = stock_info(name=stock_name,
                           close=stock_close,
                           previous_close=stock_prev_close,
                           volume=volume,
                           market_cap=market_cap)

        return stock
    except AttributeError:
        return AttributeError

# function will display stock info into GUI
def display_stock(body):
    try: 
        stock = find_stock_info(body)
        # formats each description into a str to pass onto the GUI label
        final_str = """
Company Name: {}
Close: {}  ({:+.2f})
Previous Close: {}
Volume: {:,}
Market Cap: {}\n""".format(stock.name,
                           stock.close,
                           stock.close - stock.previous_close,
                           stock.previous_close,
                           stock.volume,
                           stock.market_cap)
        
        return final_str
    # if ticker symbol cannot be found, return a message to enter another symbol
    except AttributeError:
        return 'Ticker symbol not found. Please try another.'

# function runs the main aspect of program when button is pressed
def search_button_action():
    # get user entry
    symbol = ticker_entry.get().strip().upper()
    # load body using user entry
    body = load_webpage(symbol)
    # capture stock information
    stock = display_stock(body)
    # display stock information to tkinter GUI
    stock_display["text"] = stock
 

if __name__ == "__main__":
   # set up window
    window = tk.Tk()
    window.title('Stock Info Display')

    # setting up ticker frame
    ticker_frame = tk.Frame(master=window)
    # setting up prompt
    prompt = tk.Label(master=ticker_frame, text='Enter ticker symbol')
    # setting up text box to enter ticker symbol
    ticker_entry = tk.Entry(master=ticker_frame, width=50)
    # setting search button
    search_button = tk.Button(master=ticker_frame,text='Search', command=search_button_action)

    # laying elements within ticker_frame
    prompt.grid(row=0, column=0)
    ticker_entry.grid(row=0,column=1)
    search_button.grid(row=0,column=2)

    # creating the space to display stock information
    stock_display = tk.Label(master=window, text='No Stock Information')

    # laying elements to window frame
    ticker_frame.grid(row=0,column=0)
    stock_display.grid(row=1,column=0)

    window.mainloop()