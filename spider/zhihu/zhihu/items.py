# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item,Field

class ZhihuItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    answer_count = Field()
    articles_count = Field()
    business = Field()
    major = Field()
    headline =Field()
    locations = Field()
    name = Field()
    thanked_count = Field()
    question_count = Field()
    voteup_count = Field()
    url_token = Field()
    school = Field()






