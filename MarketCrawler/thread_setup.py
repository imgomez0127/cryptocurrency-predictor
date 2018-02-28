import threading
import queue
import time
from MarketSpider import MarketSpider

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
if __name__ == '__main__':
    threads = []
    MarketSpider.page_count = 2
    directory = 'data/'
    MarketSpider.date = {'start':'20120428','end':'20180925'}
    MarketSpider.startup()
    thread_amt = 8
    q = queue.Queue()

    create_threads(thread_amt)

    queue_links()
    print(q.qsize())

    q.join()

    for _ in range(len(threads)):
        q.put(None)

    for thread in threads:
        thread.join()