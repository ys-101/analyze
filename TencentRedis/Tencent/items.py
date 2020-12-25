# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentItem(scrapy.Item):
    job_id = scrapy.Field()
    job_name = scrapy.Field()
    job_type = scrapy.Field()
    job_city = scrapy.Field()
    job_time = scrapy.Field()
    job_require = scrapy.Field()
    job_duty = scrapy.Field()









