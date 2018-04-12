# -*- coding: utf-8 -*-
import scrapy

from movie.items import MovieItem

class MovielistSpider(scrapy.Spider):
    name = 'movielist'
    allowed_domains = ['dianying.2345.com']
    start_urls = ['http://dianying.2345.com/top/']

    def parse(self, response):
    	items = []

    	lilist = response.xpath('/html/body//ul[@class="picList clearfix"]/li')

    	for li in lilist:
    		item = MovieItem()

    		item['title'] = li.xpath('./div[@class="txt"]/p[@class="pTit"]/span[@class="sTit"]//text()').extract()[0]
    		item['img'] = 'http:' + li.xpath('./div[@class="pic"]/img/@src').extract()[0]
    		if len(li.xpath('./div[@class="txt"]/p[@class="pTxt pIntroHide"]//text()').extract()) :
    			item['intro'] = li.xpath('./div[@class="txt"]/p[@class="pTxt pIntroHide"]//text()').extract()[0]
    		else:
    			item['intro'] = li.xpath('./div[@class="txt"]/p[@class="pTxt pIntroShow"]//text()').extract()[0]
    		names = ''
    		for name in li.xpath('./div[@class="txt"]/p[@class="pActor"]/a//text()'):
    			actor = name.extract()
    			names = names + '#' + actor
    		item['names'] = names
    		items.append(item)
    	return items