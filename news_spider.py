from scrapy.spiders import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from news_item import NewsItem

from IPython import embed
from IPython.terminal.embed import InteractiveShellEmbed

class NewsSpider(Spider):
    name = 'news_spider'

    start_urls = ['https://twitter.com/YahooNewsTopics']
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }

    def parse(self, response):
        tweets = '#stream-items-id p.tweet-text::text'
        for tweet in response.css(tweets):
            full_url = response.urljoin(href.extract())

            yield scrapy.Request(tweet, callback=self.parse_item)

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
