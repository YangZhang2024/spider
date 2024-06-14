import logging

import scrapy
import requests
import os
import base64

from ..constants import domain, picture_host
from ..utils import aes_cbc_pk5_padding_dec, scrtv
from ..items import PicItem


class PicSpider(scrapy.Spider):
    name = 'pictures'

    def start_requests(self):
        host = f'https://{domain}'
        urls = [host + "/cYcL3R1cGlhbi9saXN0Lmh0bWw%3D.html"]
        for url in urls:
            self.logger.info(f"========{url} schedule request")
            yield scrapy.Request(url=url, callback=self.parse_pic_category_page)

    def parse_pic_category_page(self, response):
        self.logger.info(f"========{response.url}  parse_pic_category_page")

        categories = {base64.b64decode('5ZCM5oCn576O5Zu+').decode(), base64.b64decode('576O6IW/5Lid6KKc').decode()}

        for category_selector in response.css('div.category-list a'):
            title = aes_cbc_pk5_padding_dec(category_selector.css('a::attr(title)').get())
            if title in categories:
                link = aes_cbc_pk5_padding_dec(category_selector.css('a::attr(data-link)').get())
                self.logger.info(f"++++++++schedule sub_category_page {link}")
                yield response.follow(url=link, callback=self.parse_sub_category_page, meta={'category': title})

    def parse_sub_category_page(self, response):
        self.logger.info(f"++++++++sparse_sub_category_page {response.url}")
        current_category = response.meta['category']
        current_page = response.css('div.pagination strong::text').get()
        logging.info(f"{current_category} page {current_page}")

        pic_sets = response.css('div.video-list a')
        for pic_set_selector in pic_sets:
            href = pic_set_selector.css('a::attr(href)').get()
            pic_set_name = aes_cbc_pk5_padding_dec(pic_set_selector.css('div:nth-child(2)::attr(title)').get())

            if scrtv.find_one({"pic_set_name": pic_set_name}):
                logging.info(f'{pic_set_name} has been saved ignore it')
                continue
            date = pic_set_selector.css('div.video-item-date::text').get()
            meta = {
                'name': pic_set_name,
                'date': date,
            }
            self.logger.info(f">>>>>>>>>>schedule pic_set_page {href}")
            yield response.follow(href, callback=self.parse_pic_set_page, meta=meta)
        # next page
        next_page = response.css('div.pagination a[title="下一页"]::attr(href)').get()
        if next_page and not "javascript:;" == next_page:
            yield response.follow(next_page, callback=self.parse_sub_category_page, meta={'category': current_category})

    def parse_pic_set_page(self, response):
        self.logger.info(f">>>>>>>>>>parse_pic_set_page {response.url}")
        pic_set_name = response.meta['name']
        date = response.meta['date']
        paths = response.xpath('//div[@class="tupian-detail-content"]/img/@data-pic-base64').getall()
        file_names = []
        b64_contents = []

        self.logger.info(f'#######start to download file {pic_set_name}')
        for file_path in paths:
            file_names.append(os.path.basename(file_path))
            b64_contents.append(requests.get(picture_host + file_path).text)
        self.logger.info(f'#######end download file {pic_set_name}')
        self.logger.info("get pic set %s" % pic_set_name)
        yield PicItem(pic_set_name=pic_set_name, file_names=file_names, b64_contents=b64_contents)
