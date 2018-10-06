#encoding=utf-8
import numpy as np
import pandas as pd


import scrapy


class QuotesSpider(scrapy.Spider):
    name = "aNewSpider"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    def start_requests(self):
        urls = np.array(pd.read_csv('url.csv'))[:,1].tolist()#csv转list
        urls_set = set(urls)
        urls = list(urls_set)
        urls.sort()
        urls = urls

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,headers = self.headers)


    def parse(self, response):
        title = response.css('title::text').extract_first()
        description = response.xpath('//meta[@name="description"]/@content').extract_first() if response.xpath('//meta[@name="description"]/@content').extract_first() else response.xpath('//meta[@name="Description"]/@content').extract_first()
        keyword = response.xpath('//meta[@name="keywords"]/@content').extract_first() if response.xpath('//meta[@name="keywords"]/@content').extract_first() else response.xpath('//meta[@name="Keywords"]/@content').extract_first()
        yield {
            'url': response.url,
            'title':title,
            'description': description,
            'keyword': keyword,
            }
