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

    # start_urls = [
    #     'https://twitter.com/YahooNewsTopics',
    #     'https://twitter.com/news_line_me?lang=ja',
    #     'https://twitter.com/nhk_news?lang=ja',
    #     'https://twitter.com/TwitterNewsJP?lang=ja',
    #     'https://twitter.com/mainichi',
    #     'https://twitter.com/Yomiuri_Online'
    # ]
    start_urls = [
        'https://twitter.com/YahooNewsTopics'
    ]
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }

    def parse(self, response):
        if 'YahooNews' in response.url:
            self.scrape_news('unlabelled_data/yahoo_news.json', 'YahooNews', response)
        elif 'news_line_me' in response.url:
            self.scrape_news('unlabelled_data/news_line_me.json', 'news_line_me', response)
        elif 'nhk_news' in response.url:
            self.scrape_news('unlabelled_data/nhk_news.json', 'nhk_news', response)
        elif 'TwitterNewsJP' in response.url:
            self.scrape_news('unlabelled_data/twitter_news_jp.json', 'TwitterNewsJP', response)
        elif 'mainichi' in response.url:
            self.scrape_news('unlabelled_data/mainichi.json', 'mainichi', response)
        elif 'Yomiuri_Online' in response.url:
            self.scrape_news('unlabelled_data/yomiuri_online.json', 'Yomiuri_Online', response)
        else:
            return False
            # yield scrapy.Request(tweet, callback=self.parse_item)

    def scrape_news(self, file_name, source, response):
        f = open(file_name, 'r')
        tweets = json.load(f)
        f.close()
        tweet_list = 'li.stream-item'
        for tweet_item in response.css(tweet_list):
            tweet_id = tweet_item.css('li::attr(data-item-id)').extract()[0]
            tweet_text = tweet_item.css('p.tweet-text::text').extract()[0]
            tweets[source][tweet_id] = {'content': tweet_text, 'label': None}
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
