# -*- coding: utf-8 -*-
import os
from unidecode import unidecode
import hashlib
import re

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapyAmazonPipeline(object):
    def __init__(self):
        self.output_file = "scraped_items.csv"
        self.hash_of_items_from_file = ""

    def open_spider(self, spider):
        if os.path.isfile(self.output_file):
            with open(self.output_file, "r") as handle:
                items = handle.readlines()
            self.hash_of_items_from_file = [make_hash(item.split("|")) for item in items]
        else:
            with open(self.output_file, "w") as handle:
                handle.write("")

    def process_item(self, item, spider):
        item_to_hash = [
            item['date'],
            item['id'],
            item['price'],
            item['title'],
            item['url'],
        ]
        hashed_item = make_hash(item_to_hash)
        if not hashed_item in self.hash_of_items_from_file:
            self.save_item(item)
        return item

    def save_item(self, item):
        with open(self.output_file, "a") as handle:
            output_list = [
                item['date'],
                item['id'],
                item['price'],
                item['title'],
                item['url'],
            ]
            handle.write("|".join(output_list) + "\n")


def make_hash(my_list):
    hash_input = "".join(my_list).strip()
    hash_output = hashlib.sha1()
    hash_output.update(hash_input.encode("utf-8"))
    return hash_output.hexdigest()



