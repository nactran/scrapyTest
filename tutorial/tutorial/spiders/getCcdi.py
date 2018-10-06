import scrapy
import re

class StackOverflowSpider(scrapy.Spider):
    name = 'ccdi'
    start_urls = ['http://www.ccdi.gov.cn/toutiao/']

    def parse(self, response):
        for i in range(1,50) :
            url = 'http://www.ccdi.gov.cn/toutiao/' + 'index_' + str(i) + '.html'
            #使用response.urljoin获取完整链接
            yield scrapy.Request(url, callback=self.parse_title)

    def parse_title(self, response):
       titles = [aTitle.extract() for aTitle in response.css('ul.list_news_dl li a::text')]
       for title in titles:
           if re.sub('\s','',title) == '':
               titles.remove(title)

       yield {
           'title': titles
           }







