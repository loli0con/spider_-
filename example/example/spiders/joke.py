# -*- coding: utf-8 -*-
import scrapy

from ..items import JokeItem

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"


class JokeSpider(scrapy.Spider):
    name = 'joke'
    start_urls = ['https://www.qiushibaike.com/text/page/1/']

    def parse(self, response):
        for item in response.css('.article.block'):
            joke = JokeItem()
            # joke['author'] = item.css('div>a:nth-child(2)>h2').extract_first()
            joke['author'] = item.css('.author.clearfix h2').extract_first()
            joke['content'] = item.css('.content>span').extract_first()
            yield joke

        next_url = response.css('.pagination>li:last-child a::attr(href)').extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            print(next_url)
            yield scrapy.Request(next_url, callback=self.parse, headers={"User-Agent": USER_AGENT})
