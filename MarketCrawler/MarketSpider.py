from bs4 import BeautifulSoup
import requests
import os.path
from MarketCrawler.LinkCrawler import LinkCrawler


class MarketSpider(object):
    link_file = "links.txt"
    link_file_directory = "links/"
    index_url = "https://coinmarketcap.com/"
    queue_set = set()
    page_count = 1
    hist_data = "historical-data/"
    def __init__(self, spider_id, data_directory,queue_link):
        self.__spider_id = spider_id
        self.__data_directory = data_directory
        self.__queue_link = queue_link
    @property
    def spider_id(self):
        return self.__spider_id

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
    def crawl_page(self,queue_link,**kwargs):
        if 'start' in kwargs and 'end' in kwargs:
            url_parameters = {'start':kwargs['start'], 'end':kwargs['end']}
        else:
            url_parameters = {}
        page = requests.get(queue_link+'historical-data/',params=url_parameters)
        page_soup = BeautifulSoup(page.text,"lxml")
        table_row = page_soup.find_all(['tr','td'], class_="text-right")
        crypto_trends = [trend.text.strip().split('\n') for trend in table_row]
        crypto_name = page_soup.find_all(class_='text-large')[0].contents[6].strip()
        return crypto_name,crypto_trends

    def export_data(self):
        tuple = self.crawl_page(self.__queue_link)
        full_filename = self.data_directory + str(tuple[0].replace('/',''))+ '.txt'
        if not os.path.exists(self.__data_directory):
            os.makedirs(self.__data_directory)
        if not os.path.isfile(full_filename):
            f = open(full_filename,'w')
            f.close()
        with open(full_filename,'w') as f:
            f.write(str(tuple[0]) + '\n')
            f.write("Date : Open,High,Low,Close\n")
            for item in tuple[1]:
                line = str(item[0]).strip() + ' : ' + str(','.join(item[1:-2]).strip()) + '\n'
                f.write(line)
