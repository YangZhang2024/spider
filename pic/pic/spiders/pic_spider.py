import scrapy
import requests
import os
from pymongo import MongoClient

from ..constants import domain, picture_host
from ..utils import *
from ..items import PicItem

client = MongoClient("localhost", 27017)
db = client.pic
scrtv = client.pic['4scrtv']


class PicSpider(scrapy.Spider):
    name = 'pictures'

    def start_requests(self):
        host = f'https://{domain}'
        urls = [host + "/cYcL3R1cGlhbi9saXN0Lmh0bWw%3D.html"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_pic_category_page)

    def parse_pic_category_page(self, response):
        categories = {'同性美图', '美腿丝袜'}

        for category_selector in response.css('div.category-list a'):
            title = aes_cbc_pk5_padding_dec(category_selector.css('a::attr(title)').get())
            if title in categories:
                link = aes_cbc_pk5_padding_dec(category_selector.css('a::attr(data-link)').get())
                yield response.follow(url=link, callback=self.parse_sub_category_page)

    def parse_sub_category_page(self, response):
        pic_sets = response.css('div.video-list a')
        for pic_set_selector in pic_sets:
            href = pic_set_selector.css('a::attr(href)').get()
            pic_set_name = aes_cbc_pk5_padding_dec(pic_set_selector.css('div:nth-child(2)::attr(title)').get())

            if scrtv.find_one({"pic_set_name": pic_set_name}):
                continue
            print('pic set name', pic_set_name)
            date = pic_set_selector.css('div.video-item-date::text').get()
            meta = {
                'name': pic_set_name,
                'date': date,
            }
            yield response.follow(href, callback=self.parse_pic_set_page, meta=meta)
        # next page
        next_page = response.css('div.pagination a[title="下一页"]::attr(href)').get()
        if not "javascript:;" == next_page:
            yield response.follow(next_page, callback=self.parse_sub_category_page)

    def parse_pic_set_page(self, response):
        pic_set_name = response.meta['name']
        date = response.meta['date']
        paths = response.xpath('//div[@class="tupian-detail-content"]/img/@data-pic-base64').getall()
        for file_path in paths:
            file_name = os.path.basename(file_path)
            text = requests.get(picture_host + file_path).text
            yield PicItem(pic_set_name=pic_set_name, file_name=file_name, b64_content=text)
