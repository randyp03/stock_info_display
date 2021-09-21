from bs4.element import AttributeValueWithCharsetSubstitution
import requests
from bs4 import BeautifulSoup as bs
import os

r = requests.get('https://finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch')

soup=bs(r.content)

summary_report = soup.find('div', attrs={'id':'quote-summary'})

last_close = summary_report.find('span', attrs={'class':'Trsdu(0.3s)'})
print(last_close.get_text())