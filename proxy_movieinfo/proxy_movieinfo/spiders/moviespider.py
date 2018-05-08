# -*- coding: utf-8 -*-
from scrapy import Request
import json
import scrapy
import re
from proxy_movieinfo.items import ProxyMovieinfoItem


class MoviespiderSpider(scrapy.Spider):
    name = 'moviespider'
    # allowed_domains = ['movie.douban.com']
    BASE_URL = "https://movie.douban.com/j/search_subjects?" \
               "type=%s&tag=%s&sort=%s&page_limit=%s&page_start=%s"
    TYPE = {'movie': 'movie', 'tv': 'tv'}  # 电影/电视剧
    TV_TAG = [u'热门', u'美剧', u'英剧', u'韩剧', u'日剧']
    MOVIE_TAG = [u'热门', u'经典', u'欧美', u'豆瓣高分', u'韩国', u'华语']
    SORT_TYPE = {'recommend': 'recommend', 'time': 'time', 'rank': 'rank'}  # 热度/时间/评价排序
    PAGE_LIMIT = 20  # 每页数量
    PAGE_START = 0  # 起始

    start_urls = [BASE_URL % (TYPE['tv'], TV_TAG[3], SORT_TYPE['rank'], PAGE_LIMIT, PAGE_START)]

    def start_requests(self):
        yield Request(self.start_urls[0], meta={'dont_redirect': True})

    def parse(self, response):
        # 获取名字和评分,构造请求进入详细信息页面获取其他信息。
        infos = json.loads(response.body.decode('utf-8'))
        for info in infos['subjects']:
            movie_name = '名称:'+info['title']
            movie_rate = '评分:'+info['rate']
            meta = {'_movie_name': movie_name, '_movie_rate': movie_rate}
            yield Request(info['url'], callback=self.parse_movieinfo, meta=meta)

        if len(infos['subjects']) == self.PAGE_LIMIT:
            self.PAGE_START += self.PAGE_LIMIT
            url = self.BASE_URL % (self.TYPE['tv'], self.TV_TAG[3], self.SORT_TYPE['rank'], self.PAGE_LIMIT, self.PAGE_START)
            yield Request(url)

    def parse_movieinfo(self, response):
        # 提取其他信息
        item = ProxyMovieinfoItem()
        item['movie_name'] = response.meta['_movie_name']
        item['movie_rate'] = response.meta['_movie_rate']
        movie_info = response.css('div#info').xpath('string(.)').extract_first().strip()
        item['movie_kind'] = re.search('\s+类型:.*\s+', movie_info).group(0).strip()
        item['movie_episode'] = re.search('\s+集数:.*\s+', movie_info).group(0).strip()
        item['movie_comment'] = '评价人数:'+response.css('div.rating_sum span::text').extract_first()
        yield item
