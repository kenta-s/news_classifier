from scrapy.spiders import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request

import json, codecs
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
        if 'YahooNews' in response.url:
            self.yahoo_news(response)
        else:
            return False
            # yield scrapy.Request(tweet, callback=self.parse_item)

    def yahoo_news(self, response):
        source = 'YahooNews'
        file_name = 'unlabelled_data/yahoo_news.json'
        f = open(file_name, 'r')
        tweets = json.load(f)
        f.close()
        tweet_list = 'li.stream-item'
        for tweet_item in response.css(tweet_list):
            tweet_id = tweet_item.css('li::attr(data-item-id)').extract()[0]
            tweet_text = tweet_item.css('p.tweet-text::text').extract()[0]
            tweets[tweet_id] = {'source': source, 'content': tweet_text, 'label': None}
        news_json = codecs.open(file_name, 'w', 'utf-8')
        json.dump(tweets, news_json, ensure_ascii=False)
        news_json.close()


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
