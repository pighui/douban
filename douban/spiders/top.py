# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class TopSpider(scrapy.Spider):
    name = 'top'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/top250']

    def parse(self, response):
        item = {}
        for i in range(1, 26):
            name = response.xpath("//ol[@class='grid_view']/li[%s]//span[@class='title'][1]/text()" % str(i)).extract_first()
            director_list = response.xpath("//ol[@class='grid_view']/li[%s]//p[1]/text()" % str(i)).extract()

            director = director_list[0].replace('\n', '').strip(' ').strip('...') + director_list[1].replace('\n',
                                                                                                             '').strip(
                ' ').strip('...')
            score = response.xpath(
                "//ol[@class='grid_view']/li[%s]//span[@class='rating_num']/text()" % str(i)).extract_first()
            detail = response.xpath("//ol[@class='grid_view']/li[%s]//div[@class='hd']/a/@href" % str(i)).extract_first()
            comment = response.xpath(
                "//ol[@class='grid_view']/li[%s]//span[@class='inq']/text()" % str(i)).extract_first()
            item['name'] = name
            item['director'] = director
            item['score'] = score
            item['comment'] = comment
            item['detail'] = detail
            yield item
        try:
            next_href = 'http://movie.douban.com/top250' + response.xpath("//span[@class='next']/a/@href").extract_first()
            yield Request(next_href, callback=self.parse)
        except:
            print("爬取完毕")
