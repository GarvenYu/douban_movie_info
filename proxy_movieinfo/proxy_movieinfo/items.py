# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProxyMovieinfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie_name = scrapy.Field()
    movie_kind = scrapy.Field()
    movie_episode = scrapy.Field()  # 集数
    movie_rate = scrapy.Field()
    movie_comment = scrapy.Field()  # 评价人数
