"""
    A module that contains the class for a webcrawler which finds all the CryptoCurrency data hosted on coinmarketcap
    By Ian Gomez
"""
from bs4 import BeautifulSoup
import requests
import os.path
from .LinkCrawler import LinkCrawler
import csv

class MarketSpider(object):
    link_file = "links.txt"
    link_file_directory = "links/"
    index_url = "https://coinmarketcap.com/"
    queue_set = set()
    page_count = 1
    hist_data = "historical-data/"
    date = {}

    def __init__(self, spider_id, data_directory,queue_link):
        self.__spider_id = spider_id
        self.__data_directory = data_directory
        self.__queue_link = queue_link

    @property
    def spider_id(self):
        return self.__spider_id

    @spider_id.setter
    def spider_id(self,spider_id):
        self.__spider_id = spider_id
        
    @property
    def queue_link(self):
        return self.__queue_link

    @property
    def data_directory(self):
        return self.__data_directory

    @staticmethod
    def startup():
        full_filename = MarketSpider.link_file_directory + MarketSpider.link_file
        if not os.path.exists(MarketSpider.link_file_directory):
            os.makedirs(MarketSpider.link_file_directory)
        if not os.path.isfile(full_filename):
            f = open(full_filename, 'w')
            f.close()
        LinkCrawler(MarketSpider.index_url,MarketSpider.page_count,MarketSpider.link_file,MarketSpider.link_file_directory).export_links()
        with open(full_filename,'rt') as f:
            for line in f:
                MarketSpider.queue_set.add(line.replace('\n',''))

    def crawl_page(self):
        page = requests.get(self.__queue_link+'historical-data/',params=MarketSpider.date)
        page_soup = BeautifulSoup(page.text,"lxml")
        table_row = page_soup.find_all(['tr','td'], class_="text-right")
        crypto_trends = [trend.text.strip().split('\n') for trend in table_row]
        if(crypto_trends == []):
            raise ValueError("This cryptocurrency does not exist in the CoinMarketCap database")
        crypto_name = self.__queue_link[37:-1]
        return crypto_name,crypto_trends

    def export_data(self):
        tuple = self.crawl_page()
        full_filename = self.data_directory + str(tuple[0].replace('/',''))+ '.csv'
        if not os.path.exists(self.__data_directory):
            os.makedirs(self.__data_directory)
        if not os.path.isfile(full_filename):
            f = open(full_filename,'w')
            f.close()
        with open(full_filename,'w') as f:
            f.write("Date,Open,High,Low,Close,Volume,Market Cap\n")
            for item in tuple[1]:
                line = str(item[0].replace(',', '')).strip() + ',' + str(','.join([market_value.replace(',','') for market_value in item[1:]]).strip()) + '\n'
                f.write(line)
    