import requests
from bs4 import BeautifulSoup
import sys
from urllib3.exceptions import HTTPError
class TestCrawler(object):
    def __init__(self, request_link):
        if isinstance(request_link, str):
            self.__request_link = request_link
        else:
            raise TypeError("the Request_link is not a string")
        try:
            self.__webpage = requests.get(self.__request_link, auth=('user', 'pass'))
        except:
            raise requests.RequestException("The webpage either, does not exist or the request has failed")
        self.__soup = BeautifulSoup(self.__webpage.text, 'html.parser')
        self.__dataset = []

    @property
    def request_link(self):
        return self.__request_link

    @request_link.setter
    def request_link(self, request_link):
        self.__request_link = request_link

    @property
    def webpage(self):
        return self.__webpage

    @property
    def soup(self):
        return self.__soup

    def filter_tags(self, tag_name):
        context = self.__soup.find_all(tag_name)
        text = ""
        for item in context:
            text += str(item) + " "
        self.__soup = BeautifulSoup(text, "html.parser")

    def filter_id(self, id_name):
        context = self.__soup.find(id=id_name)

    def filter_class(self, class_name):
        context = self.__soup.find_all(class_=class_name)
        text = ""
        for item in context:
            text += str(item) + " "
        self.__soup = BeautifulSoup(text, "html.parser")

    def reset_soup(self):
        self.__soup = BeautifulSoup(self.__webpage.text, 'html.parser')

    def __str__(self):
        return str(self.soup)


if __name__ == '__main__':
    test = TestCrawler("https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20180126&end=20180201")
    test.filter_tags("tbody")
    test.filter_class("text-right")
    print(test)








