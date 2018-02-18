import requests
from bs4 import BeautifulSoup
import os.path

class WebCrawler:
    def __init__(self, request_link):
        if isinstance(request_link, str):
            self.__request_link = request_link
        else:
            raise TypeError("the Request_link is not a string")
        try:
            self.__webpage = requests.get(self.__request_link, auth=('user', 'pass'))
        except:
            raise requests.RequestException("The webpage either, does not exist or the request has failed")

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
    def dataset(self):
        return self.__dataset

    @dataset.setter
    def dataset(self,data):
        self.__dataset = data

    def appenddata(self,data):
        self.__dataset.append(data)

    def find_tags(self,tag_name,soup):
        context = soup.find_all(tag_name)
        text = ""
        for item in context:
            text += str(item) + " "
        return text
    def filter_tags(self, tag_name,soup):
        context = soup.find_all(tag_name)
        text = ""
        for item in context:
            text += str(item) + " "
        return BeautifulSoup(text, "lxml")

    def find_id(self,id_name,soup):
        return soup.find(id=id_name)

    def filter_id(self, id_name,soup):
        context = BeautifulSoup(soup.find(id=id_name),"lxml")
        return context

    def filter_class(self, class_name,soup):
        context = soup.find_all(class_=class_name)
        text = ""
        for item in context:
            text += str(item) + " "
        return BeautifulSoup(text, "lxml")
    def find_class(self,class_name,request):
        context = request.find_all(class_=class_name)
        text = ""
        for item in context:
            text += str(item) + " "
        return text
    def filter_CSS_selector(self,css_selector,soup):
        context = soup.select(css_selector)
        text = ""
        for item in context:
            text += str(item) + " "
        return BeautifulSoup(text, "lxml")
    def find_CSS_selector(self,css_selector,soup):
        context = soup.select(css_selector)
        text = ""
        for item in context:
            text += str(item) + " "
        return text
    def reset_soup(self,webpage_text):
        return BeautifulSoup(webpage_text, 'lxml')

    def make_query(self,link,query_extension,query):
        if isinstance(query_extension,str) != True:
            raise TypeError("query_extension must be type string")
        if isinstance(query, dict) != True:
            raise TypeError()
        url = link + query_extension
        return BeautifulSoup(requests.get(url, params=query))

    def export_data(self,filename, input_dictionary):
        if isinstance(filename, str) != True:
            raise TypeError("filename must be a string")
        if isinstance(input_dictionary, dict) != True:
            raise TypeError("input_dictionary must be a dictionary")
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.isfile('data/' + filename):
            f = open('data/' + filename,'w')
            f.close()
        f = open('data/' + filename,'w')

        for key,crypto_dict in input_dictionary.items():
            f.write(str(key) + '\n')
            title = "Date : Open,High,Low,Close\n"
            f.write(title)
            for item,data in crypto_dict.items():
                line = str(item).strip() + " : " + ",".join(data[:-2]).strip() + '\n'
                f.write(line)
        f.close()
    def find_links(self,request_text):
        filtered_links = BeautifulSoup(request_text, "lxml").find_all('a')
        return filtered_links
    def find(self,find_request,request_text):
        filtered_text = BeautifulSoup(request_text,"lxml").find_all(find_request)

    def __str__(self):
        return str(self.request_link)
if __name__ == "__main__":
    test = WebCrawler("https://coinmarketcap.com/")
    test.dataset = BeautifulSoup(test.webpage.text,"lxml")
    print(test.filter_class("currency-name-container",test.dataset))
