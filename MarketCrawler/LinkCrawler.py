"""
    A module that contains the class for a webcrawler which finds all the CryptoCurrency links on the current coinmarketcap page
"""
import requests
from bs4 import BeautifulSoup
import os.path
from math import ceil

class LinkCrawler(object):
    def __init__(self,index_url,page_amt,filename,dirname):
        self.__index_url = index_url
        self.__filename = filename
        self.__page_amt = page_amt
        self.__dirname = dirname

    @property
    def index_url(self):
        return self.__index_url

    @index_url.setter
    def index_url(self,index_url):
        self.__index_url = index_url
        self.export_links

    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self,filename):
        self.__filename = filename
        self.export_links()

    @property
    def dirname(self):
        return self.__dirname

    @dirname.setter
    def dirname(self):
        return self.__dirname
        self.export_links()

    @property
    def page_amt(self):
        return self.__page_amt

    @page_amt.setter
    def page_amt(self,page_count):
        self.__page_amt = page_amt
        self.export_links()

    @property
    def full_filename(self):
        if self.__dirname == '/':
            return self.__filename
        return self.__dirname + self.__filename
        self.find_links()
        
    def find_links(self,index_url,page_amt):
        a_tag_list = []
        links_list = []
        for i in range(1,page_amt+1):
            index_page = requests.get(index_url + str(i))
            a_tag_list += BeautifulSoup(index_page.text,"lxml").find_all(class_="currency-name-container")
        for a_tag in a_tag_list:
            links_list.append(index_url[:-1] + a_tag.get('href'))
        return links_list[:self.__page_amt]

    def export_links(self):
        links_list = self.find_links(self.__index_url, ceil(self.__page_amt/100))
        if not os.path.exists(self.__dirname):
            os.makedirs(self.__dirname)
        if not os.path.isfile(self.__filename):
            f = open(self.full_filename, "w")
            f.close()
        f = open(self.full_filename,'w')
        f.write('\n'.join(links_list))
        f.close()

    def append_links(self):
        links_list = self.find_links(self.__index_url, ceil(self.__page_amt/100))
        if not os.path.exists(self.__dirname):
            os.makedirs(self.__dirname)
        if not os.path.isfile(self.__filename):
            f = open(self.full_filename, "w")
            f.close()
        f = open(self.full_filename, "a")
        f.write('\n'.join(links_list))
        f.close()

    def read_links(self):
        f = open(self.full_filename,"r")
        links_list = []
        for line in f:
            links_list.append(line.replace('\n',''))
        f.close()
        return links_list
