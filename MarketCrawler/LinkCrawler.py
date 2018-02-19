import requests
from bs4 import BeautifulSoup
import os.path


class LinkCrawler(object):
    def __init__(self,index_url,page_count,filename,dirname):
        self.__index_url = index_url
        self.__filename = filename
        self.__page_count = page_count
        self.__dirname = dirname

    @property
    def index_url(self):
        return self.__index_url

    @index_url.setter
    def index_url(self,index_url):
        self.__index_url = index_url

    @property
    def filename(self):
        return self.__filename
    @filename.setter
    def filename(self,filename):
        self.__filename = filename

    @property
    def dirname(self):
        return self.__dirname

    @dirname.setter
    def dirname(self):
        return self.__dirname

    @property
    def page_count(self):
        return self.__page_count

    @page_count.setter
    def page_count(self,page_count):
        self.__page_count = page_count

    @property
    def full_filename(self):
        if self.__dirname == '/':
            return self.__filename
        return self.__dirname + self.__filename

    def find_links(self,index_url,page_count):
        a_tag_list = []
        links_list = []
        for i in range(1,page_count+1):
            index_page = requests.get(index_url + str(i))
            a_tag_list += BeautifulSoup(index_page.text,"lxml").find_all(class_="currency-name-container")
        for a_tag in a_tag_list:
            links_list.append(index_url[:-1] + a_tag.get('href'))
        return links_list

    def export_links(self):
        links_list = self.find_links(self.__index_url,self.__page_count)
        if not os.path.exists(self.__dirname):
            os.makedirs(self.__dirname)
        if not os.path.isfile(self.__filename):
            f = open(self.full_filename, "w")
            f.close()
        f = open(self.full_filename,'w')
        f.write('\n'.join(links_list))
        f.close()

    def append_links(self):
        links_list = self.find_links(self.__index_url, self.__page_count)
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


