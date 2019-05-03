# -*- coding: UTF-8 -*-
'''
This spider extracts specific content from given movie links which can be 
accessed from Redis Database by redis_key "movie_links" and stores the data
to HBase.
Moreover, this spider should export link to more reviews to Redis Database
as redis_key "more_reviews".
'''

import os
import sys
import scrapy
from scrapy_redis.spiders import RedisSpider
from douban_crawler.items import MovieItem


class MovieContentSpider(RedisSpider):
    name = "movieContent"
    redis_key = "movie_links"

    def parse(self, response):
        host = self.settings['REDIS_HOST']
        item = MovieItem()
        cid = response.xpath('//div[@class="lister-item mode-detail imdb-user-review  with-image"]/@data-review-id').extract()[0]
        rate = response.xpath('//div[@class="ipl-ratings-bar"]/span/span/text()').extract()[0]
        try:
            content = response.xpath('//div[@class="text show-more__control"]/text()').extract()[0]
        except IndexError:
            content = ''
        item['CommentId'] = cid
        item['Content'] = content
        item['Rate'] = rate

        yield item
