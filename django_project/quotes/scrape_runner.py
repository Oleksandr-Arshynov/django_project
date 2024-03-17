from scrapy.crawler import CrawlerProcess
from import_quotes import QuotesSpider 

def run_scraper():
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()

if __name__ == '__main__':
    run_scraper()
