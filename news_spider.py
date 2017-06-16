from scrapy.spiders import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from news_item import NewsItem

import json
# usage of json is below... (I'm a beginner in Python :P)
#
# foo = open('categories.json', 'r')
# bar = json.load(foo)

from IPython import embed
from IPython.terminal.embed import InteractiveShellEmbed

class NewsSpider(Spider):
    name = 'news_spider'

    start_urls = ['https://twitter.com/YahooNewsTopics']
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }

    def parse(self, response):
        tweet_list = 'li.stream-item'
        # embed()
        for tweet_item in response.css(tweet_list):
            tweet_id = tweet_item.css('li::attr(data-item-id)').extract()
            tweet_text = tweet_item.css('p.tweet-text::text').extract()

        # news_json = open('yahoonews.json', 'w')
            # yield scrapy.Request(tweet, callback=self.parse_item)

    def parse_item(self, response):
        return True
        # TODO: implement

        # urls = []
        # for href in response.css(''):
        #     full_url = response.urljoin(href.extract())
        #     urls.append(full_url)

        # yield {
        #     'title': response.css('h1::text').extract(),
        #     'urls': urls,
        # }

# scrapy runspider news_spider.py -o foo.json
