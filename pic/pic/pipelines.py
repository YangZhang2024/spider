# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .utils import b64_to_pic
import os


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
        file_name = adapter.get('file_name')
        d = 'E:\\data\\pictures\\' + pic_set_name + '\\'

        folder = os.path.exists(d)
        if not folder:
            os.mkdir(d)

        b64_to_pic(adapter.get('b64_content'), d, file_name)
        return item
