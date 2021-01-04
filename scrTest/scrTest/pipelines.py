# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

class ScrtestPipeline(ImagesPipeline):
    # 返回图片连接
    def get_media_requests(self, item, info):
        print("path:" + item["path"] + "    name:" + item["name"])
        return scrapy.Request(item["link"])

    # 自定义下载路径
    def file_path(self, request, response=None, info=None, *, item=None):
        return r"pic\\" + item["path"] + "\\" + item["name"] + ".jpg"

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        adapter = ItemAdapter(item)
        adapter['image_paths'] = image_paths
        return item
