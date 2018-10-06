"""
   A module which gather all the data for the cryptocurrencies on coinmarket cap 
"""
import queue
import time
import threading
from MarketSpider import MarketSpider
def gatherData(page_count = 1, thread_amt = 4):
    """
        returns the pages starting at the most popular CryptoCurrency and ends at the page_count indexed cryptocurrency
    """
    def worker(thread_name):
        while True:
            link = q.get()

            if link == None:
                print(thread_name + " is exiting")
                break
            spider = MarketSpider(thread_name,directory,link)
            spider.export_data()
            print(thread_name + " is working")
            q.task_done()

    def create_threads(thread_amt):
        for i in range(thread_amt):
            thread = threading.Thread(daemon=True,target=worker, args=["Thread "+ str(i+1)])
            thread.start()
            threads.append(thread)

    def queue_links():
        for link in MarketSpider.queue_set:
            q.put(link)

    threads = []
    MarketSpider.page_count = 1
    directory = 'data/'
    MarketSpider.date = {'start':'20120428','end':time.strftime("%Y%m%d")}
    MarketSpider.startup()
    q = queue.Queue()

    create_threads(thread_amt)

    queue_links()

    q.join()

    for _ in range(len(threads)):
        q.put(None)

    for thread in threads:
        thread.join()
if __name__ == '__main__':
    gatherData(thread_amt = 8)