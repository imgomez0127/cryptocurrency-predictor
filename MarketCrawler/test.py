import time
import requests
from bs4 import BeautifulSoup
x = time.time()
BeautifulSoup(requests.get("https://coinmarketcap.com/currencies/bitcoin/historical-data/").text, 'lxml')
print(time.time()-x)