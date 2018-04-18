# -*- coding: utf-8 -*-
from scrapy import Request
import json
import scrapy
from proxy_movieinfo.proxy_movieinfo.items import ProxyMovieinfoItem


class MoviespiderSpider(scrapy.Spider):
    name = 'moviespider'
    # allowed_domains = ['movie.douban.com']
    BASE_URL = "https://movie.douban.com/j/search_subjects?" \
               "type=%s&tag=%s&sort=%s&page_limit=%s&page_start=%s"
    TYPE = {'movie': 'movie', 'tv': 'tv'}  # 电影/电视剧
    TV_TAG = ['热门', '美剧', '英剧', '韩剧', '日剧']
    MOVIE_TAG = ['热门', '经典', '欧美', '豆瓣高分', '韩国', '华语']
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
            movie_name = info['title']
            movie_rate = info['rate']
            meta = {'_movie_name': movie_name, '_movie_rate': movie_rate}
            yield Request(info['url'], callback=self.parse_movieinfo, meta=meta)

    def parse_movieinfo(self, response):
        # 提取其他信息
        pass