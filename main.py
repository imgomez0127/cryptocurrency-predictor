from MarketCrawler.thread_setup import gatherData
if __name__ == "__main__":
	page_count = int(input("Insert the amount of pages you want to crawl: ").strip())
	thread_amt = int(input("Insert the amount of threads you want to use: ").strip())
	gatherData(page_count,thread_amt)
