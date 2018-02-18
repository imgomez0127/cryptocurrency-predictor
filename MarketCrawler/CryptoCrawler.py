from WebCrawler import WebCrawler
import requests
from bs4 import BeautifulSoup
import os.path
class CryptoCrawler(WebCrawler):
    def __init__(self,webpage_num):
        super().__init__("https://coinmarketcap.com/")
        self.__url_extensions = "historical-data/"
        self.__webpage_num = webpage_num
        self.__webpage_soups = {}
        self.__webpage_links = {}
        self.__crypto_data = {}
        self.get_crypto_links()

    def get_crypto_links(self):
        market_list = []
        links = []
        coin_title = []
        for i in range(1,self.__webpage_num+1):
            market_list.append("https://coinmarketcap.com/"+str(i))
        for page in market_list:
            page_link = requests.get(page)
            page_soup = BeautifulSoup(page_link.text,"lxml")
            links += page_soup.find_all("a",class_="currency-name-container")
            coin_title += page_soup.find_all("img",class_="currency-logo-sprite")
        for i in range(len(links)):
            self.__webpage_links[coin_title[i].get('alt')] = "https://coinmarketcap.com/" + links[i].get('href') + self.__url_extensions
        for key,page in self.__webpage_links.items():
            page_data = requests.get(page)
            self.__webpage_soups[key] = BeautifulSoup(page_data.text,"lxml")
    def get_crypto_data(self):
        for key,page in self.__webpage_soups.items():
            filtered_page = page.find_all(['tr','td'], class_="text-right")
            crypto_trends = {}
            for item in filtered_page:
                table_row = item.text.strip().split('\n')
                crypto_trends[table_row[0]] = table_row[1:]
            self.__crypto_data[key] = crypto_trends
    def export(self):
        for key,values in self.__crypto_data.items():
            self.export_data(str(key)+'.txt',{key:values})
    @property
    def webpage_soups(self):
        return self.__webpage_soups

    @property
    def webpage_num(self):
        return self.__webpage_num

    @webpage_num.setter
    def webpage_num(self,webpage_num):
        self.__webpage_num = webpage_num
        self.get_crypto_links()
    @property
    def webpage_links(self):
        return self.__webpage_links
    @property
    def crypto_data(self):
        return self.__crypto_data
if __name__ == "__main__":
    test = CryptoCrawler(1)
    test.get_crypto_data()
    test.export()
