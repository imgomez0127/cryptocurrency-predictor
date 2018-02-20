import threading
import queue
import time
from MarketCrawler.MarketSpider import MarketSpider

if __name__ == "__main__":
    MarketSpider.page_count = 4
    MarketSpider.startup()
    directory = "data/"
    thread_amt = 8
    MarketSpider.date = {'start':'20180214','end':20180220}
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
    q = queue.Queue()
    threads = []
    for link in MarketSpider.queue_set:
        q.put(link)
    for i in range(thread_amt):
        thread = threading.Thread(daemon=True,target=worker, args=["Thread "+ str(i+1)])
        thread.start()
        threads.append(thread)
    q.join()
    for _ in range(len(threads)):
        q.put(None)
    for thread in threads:
        thread.join()
