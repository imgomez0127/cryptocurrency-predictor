import requests
from bs4 import BeautifulSoup
import sys
import re
class TestCrawler(object):
    def __init__(self,request_link):
        if isinstance(request_link,str):
            self.__request_link = request_link
        else:
            raise TypeError("the Request_link is not a string")
            sys.exit(1)
        try:
            self.__webpage = requests.get(self.__request_link)
        except TypeError:
            raise TypeError("The Webpage does not exist")
            sys.exit(1)
        self.__html_doc = self.__webpage.text
        self.__soup = BeautifulSoup(self.__webpage.text, 'html.parser')

    @property
    def request_link(self):
        return self.__request_link

    @request_link.setter
    def request_link(self,request_link):
        self.__request_link=request_link

    @property
    def webpage(self):
        return self.__webpage

    @property
    def html_doc(self):
        return self.__html_doc

    @property
    def soup(self):
        return self.__soup

    def search_tags(self, tag_name):
        return self.__soup.find_all(tag_name)

    def search_id(self,id_name):
        return self.__soup.find(id=id_name)

if __name__ == '__main__':
    test_crawler = TestCrawler("http://www.coretcg.com/buylist#%7B%22q%22%3A%22Blue%20eyes%22%7D")
    search_regex = test_crawler.soup.find_all(re.compile("[$0-9]+"))
    for item in search_regex:
        print(item.text)



