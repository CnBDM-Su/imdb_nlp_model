'''
This spider crawls iterates index pages and then release movie links 
to Redis Database with redis_key: "movie_links"
'''

import os
import scrapy
import sys
from scrapy_redis.spiders import RedisSpider

class DoubanMovieSpider(scrapy.Spider):
    start_urls = ["https://www.imdb.com/title/tt6857112/reviews?sort=helpfulnessScore&dir=asc&ratingFilter=0"]
    name = "movieLinks"
    
    def parse(self,response):
        base = "https://www.imdb.com/title/tt6857112/reviews/_ajax?sort=helpnessScore&dir=asc&ratingFilter=0&ref_=undifined&paginationKey="
        host = self.settings['REDIS_HOST']
        lists = response.xpath('//div[@class="lister-item-content"]/a/@href').extract()
        for li in lists:
            li = response.urljoin(li)
            command = "redis-cli -h " + host + " lpush movie_links " + li
            os.system(command)
        
        try:
            url1 = response.xpath('//div[@class="load-more-data"]/@data-key').extract()[0]
        except:
            return
        url = base + url1
        yield scrapy.Request(url, callback=self.parse)
        