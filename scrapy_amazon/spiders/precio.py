# -*- coding: utf-8 -*-
from datetime import date
import re

import scrapy
from scrapy_amazon.items import ScrapyAmazonItem


class PrecioSpider(scrapy.Spider):
    name = "precio"
    allowed_domains = ["www.amazon.co.uk"]
    start_urls = (
        'http://www.amazon.co.uk/',
    )

    def __init__(self, item_id=''):
        self.item_id = item_id
        url = self.start_urls[0] + "/gp/offer-listing/" + self.item_id 
        url += "/ref=dp_olp_used?ie=UTF8&condition=used"
        self.start_urls = [url]

    def parse(self, response):
        sel = response.xpath

        condition = sel("//h3[contains(@class, 'olpCondition')]/text()").extract()[0].strip()
        delivery = sel("//div[contains(@class, 'olpDeliveryColumn')]/ul/li/span/text()").extract()[1].strip()
        today = date.today()

        item = ScrapyAmazonItem()

        item['title'] = sel("//title/text()").re("Buying Choices: (.+)")[0]
        item['price'] = "gb" + sel("//span[contains(@class, 'olpOfferPrice')]/text()").re("[0-9]+\.?[0-9]*")[0]
        item['seller'] = sel("//p[contains(@class, 'olpSellerName')]/span/a/text()").extract()[0]
        item['condition'] = re.sub("\s+", " ", condition)
        item['delivery'] = re.sub("\s+", " ", delivery)
        item['date'] = date.strftime(today, "%Y-%m-%d")
        yield item
