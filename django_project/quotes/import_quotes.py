import json
import scrapy
from itemadapter import ItemAdapter
# from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field

# from .models import Author, Quote


class QuoteItem(Item):
    quote = Field()
    author = Field()
    tags = Field()


class AuthorItem(Item):
    fullname = Field()
    born_date = Field()
    born_location = Field()
    description = Field()


class DataPipline:
    quotes = []
    authors = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'fullname' in adapter.keys():
            self.authors.append(dict(adapter))
        if 'quote' in adapter.keys():
            self.quotes.append(dict(adapter))

    def close_spider(self, spider):
        with open('quotes.json', 'w') as file:
            json.dump(self.quotes, file, ensure_ascii=False, indent=2)
            
        with open('authors.json', 'w') as file:
            json.dump(self.authors, file, ensure_ascii=False, indent=2)



class QuotesSpider(scrapy.Spider):
    name = "get_quotes"
    start_urls = ["http://127.0.0.1:8000/"]

    custom_settings = {"ITEM_PIPELINES": {DataPipline: 300}}

    def parse(self, response, **kwargs):
        for q in response.xpath("/html//div[@class='quote']"):
            quote = q.xpath("span[@class='text']/text()").get().strip()
            author = q.xpath("span/small[@class='author']/text()").get().strip()
            tags = q.xpath("div[@class='tags']/a/text()").extract()
           
            yield QuoteItem(quote=quote, author=author, tags=tags)
            yield response.follow(url=self.start_urls[0] + q.xpath("span/a/@href").get(), callback=self.parse_author)

        next_link = response.xpath("/html//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    
    def parse_author(cls, response, **kwargs):
        content = response.xpath("/html//div[@class='author-details']")
        fullname = content.xpath("h1[@class='author-titlle']/text()").get().strip()
        born_date = content.xpath("p/strong[contains(text(), 'Born:')]/following-sibling::text()").get().strip()
        born_location = content.xpath("p/strong[contains(text(), 'Born location:')]/following-sibling::text()").get().strip()
        description = content.xpath("p/strong[contains(text(), 'Description:')]/following-sibling::text()").get().strip()

        yield AuthorItem(fullname=fullname, born_date=born_date, born_location=born_location, description=description)

