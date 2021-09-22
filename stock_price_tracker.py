import requests
from bs4 import BeautifulSoup as bs
import os

symbol = input('Enter ticker symbol: ')
r = requests.get('https://finance.yahoo.com/quote/' + symbol + '?p=' + symbol + '&.tsrc=fin-srch')

soup=bs(r.content, features="html5lib")

company_name = soup.find('h1', attrs={'class':'D(ib) Fz(18px)'})

stock_heading = soup.find('div', attrs={'data-reactid':'47'})
stock_close = stock_heading.find('span',attrs={'class':'Trsdu(0.3s)'})

left_side_report = soup.find('table', attrs={'data-reactid':'91'})
right_side_report = soup.find('table', attrs={'data-reactid':'132'})

table_1 = left_side_report.find_all('span', attrs={'class':'Trsdu(0.3s)'})
table_2 = right_side_report.find_all('span', attrs={'class':'Trsdu(0.3s)'})

table_1_stats = []
for stat in table_1:
     table_1_stats.append(stat.get_text())
    
table_2_stats = []
for stat in table_2:
    table_2_stats.append(stat.get_text())

all_stats = table_1_stats + table_2_stats

print('Company Name: ', company_name.get_text())
print('Stock Close Price: ', stock_close.get_text())
print('Table 1 list: ' , table_1_stats)
print('Table 2 list: ' , table_2_stats)
print('All stats: ', all_stats)