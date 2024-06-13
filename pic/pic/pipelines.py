# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .utils import save_pictures, scrtv
import os
from .constants import pic_dir


class PicPipeline:
    collection_name = "scrapy_items"

    # def open_spider(self, spider):
    #     self.client = pymongo.MongoClient(self.mongo_uri)
    #     self.db = self.client[self.mongo_db]
    #
    # def close_spider(self, spider):
    #     self.client.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        pic_set_name = adapter.get('pic_set_name')
        file_names = adapter.get('file_names')
        b64_contents = adapter.get('b64_contents')

        directory = os.path.normpath(os.path.join(pic_dir, pic_set_name))
        save_pictures(directory, pic_set_name, file_names, b64_contents)
        scrtv.insert_one({'pic_set_name': pic_set_name})
        logging.info(f"process item {pic_set_name}")
        return item
