import requests
from bs4 import BeautifulSoup


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

    @property
    def dataset(self):
        return self.__dataset

    @dataset.setter
    def dataset(self, data):
        self.__dataset = data

    def appenddata(self, data):
        self.__dataset.append(data)

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

    def filter_CSS_selector(self, css_selector):
        context = self.__soup.select(css_selector)
        text = ""
        for item in context:
            text += str(item) + " "
        self.__soup = BeautifulSoup(text, "html.parser")

    def reset_soup(self):
        self.__soup = BeautifulSoup(self.__webpage.text, 'html.parser')

    def make_query(self, query_extension, query):
        if isinstance(query_extension, str) != True:
            raise TypeError("query_extension must be type string")
        if isinstance(query, dict) != True:
            raise TypeError()
        url = self.__request_link + query_extension
        self.__webpage = requests.get(url, params=query)
        self.__soup = BeautifulSoup(self.__webpage)

    def export_data(self, filename, input_dictionary):
        if isinstance(filename, str) != True:
            raise TypeError("filename must be a string")
        if isinstance(input_dictionary, dict) != True:
            raise TypeError("input_dictionary must be a dictionary")
        f = open(filename, 'w')
        title = "Date : Open,High,Low,Close,Volume,Market Cap\n"
        f.write(title)
        for key, item in input_dictionary.items():
            line = str(key).strip() + " : " + str(item).strip() + '\n'
            f.write(line)
        f.close()

    def __str__(self):
        return str(self.soup)

if __name__ == '__main__':
    test = TestCrawler("https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20180126&end=20180201")
    test.filter_tags("tbody")
    test.filter_class("text-right")
    print(test)
