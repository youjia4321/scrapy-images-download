# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from urllib import request
from scrapy.pipelines.images import ImagesPipeline
from bmw import settings

class BmwPipeline(object):

    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
        if not os.path.exists(self.path):
            os.mkdir(self.path)



    def process_item(self, item, spider):
        category = item['category']
        urls = item['urls']
        category_path = os.path.join(self.path, category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)
        for url in urls:
            image_name = url.split("_")[-1]
            request.urlretrieve(url, os.path.join(category_path, image_name))
        # 传统的方式下载图片

        return item


class BmwImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        request_objs = super(BmwImagesPipeline, self).get_media_requests(item, info)
        for request_obj in request_objs:
             request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        path = super(BmwImagesPipeline, self).file_path(request, response, info)
        category = request.item.get('category')
        images_store = settings.IMAGES_STORE
        category_path = os.path.join(images_store, category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)
        image_name = path.replace("full/", "")
        image_path = os.path.join(category_path, image_name)
        return image_path

