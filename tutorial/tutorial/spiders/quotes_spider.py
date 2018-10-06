#encoding=utf-8
import numpy as np
import pandas as pd


import scrapy


class QuotesSpider(scrapy.Spider):
    name = "aNewSpider"
    def start_requests(self):
        urls = np.array(pd.read_csv('url.csv'))[:,1].tolist()#csv转list
        urls_set = set(urls)
        urls = list(urls_set)
        urls.sort()
        urls = urls

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        title = response.css('title::text').extract_first()
        description = response.xpath('//meta[@name="description"]/@content').extract_first()
        keyword = response.xpath('//meta[@name="keywords"]/@content').extract_first()
        yield {
            'url': response.url,
            'title':title,
            'description': description,
            'keyword': keyword,
            }
