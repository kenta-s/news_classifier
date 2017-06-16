# pip install Scrapy
from scrapy.item import Item, Field

class NewsItem(Item):
    id = Field()
    content = Field()
