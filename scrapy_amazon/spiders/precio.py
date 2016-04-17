# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy.http import Request

from scrapy_amazon.items import ScrapyAmazonItem


class PrecioSpider(scrapy.Spider):
    name = "precio"
    allowed_domains = ["amazon.co.uk", "amazon.com"]
    start_urls = (
        'http://www.amazon.com/',
    )

    def __init__(self, item_id=''):
        self.item_id = item_id
        listing_url = "{0}s/ref=nb_sb_noss_2?field-keywords={1}".format(self.start_urls[0],
                                                                        self.item_id)
        self.start_urls = [listing_url]
        super(PrecioSpider, self).__init__()

    def parse(self, response):
        item_urls = response.xpath("//a[contains(@class, 's-access-detail-page')]/@href").extract()
        for url in item_urls:
            yield  Request(url, callback=self.parse_item)

    def parse_item(self, response):
        item = ScrapyAmazonItem()
        item['price'] = response.xpath("//span[@id='priceblock_ourprice']/text()").extract_first()
        item['date'] = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
        item['title'] = response.xpath("//span[@id='productTitle']/text()").extract_first()
        item['url'] = response.url
        yield item
