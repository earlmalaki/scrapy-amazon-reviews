########################################
# Author : Earl Timothy D. Malaki
# User Experience Designer
# Plaza 2 6th Floor C'10 6
# Lexmark Research and Development Cebu
########################################

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
from scrapy_amazon_reviews import product_list
from scrapy_amazon_reviews import utility

from pydispatch import dispatcher
from scrapy import signals
from scrapy.exporters import CsvItemExporter


class CsvExportPipeline(object):
    SaveTypes = ["TrckedPrdctsCX", "AllPrdcts", "PBIRprt"]
    tracked_prdcts = []

    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.files = {}
        self.tracked_prdcts = product_list.get_tracked_products()

    def spider_opened(self, spider):
        dtnow = str(datetime.datetime.now().strftime("%Y-%m-%dT%I-%M"))
        # self.files = dict([ (name, open(spider.name+'/Scrapy_AmazonReviews_'+name+'_'+dtnow +'.csv','w+b')) for name in self.SaveTypes ])
        self.files = {
            self.SaveTypes[0]: open(
                spider.name
                + "/Scrapy_AmazonReviews_"
                + self.SaveTypes[0]
                + "_"
                + dtnow
                + ".csv",
                "w+b",
            ),
            self.SaveTypes[1]: open(
                spider.name
                + "/Scrapy_AmazonReviews_"
                + self.SaveTypes[1]
                + "_"
                + dtnow
                + ".csv",
                "w+b",
            ),
            self.SaveTypes[2]: open(
                spider.name + "/Scrapy_AmazonReviews_" + self.SaveTypes[2] + ".csv",
                "w+b",
            ),
        }
        self.exporters = {
            self.SaveTypes[0]: CsvItemExporter(
                self.files[self.SaveTypes[0]],
                fields_to_export=utility.EXPRTFLDS_SELECTED,
            ),
            self.SaveTypes[1]: CsvItemExporter(
                self.files[self.SaveTypes[1]],
                fields_to_export=utility.EXPRTFLDS_SELECTED,
            ),
            self.SaveTypes[2]: CsvItemExporter(
                self.files[self.SaveTypes[2]], fields_to_export=utility.EXPRTFLDS_ALL
            ),
        }

        # self.exporters = dict([ (name,CsvItemExporter(self.files[name])) for name in self.SaveTypes ])
        [e.start_exporting() for e in self.exporters.values()]

    def spider_closed(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    def process_item(self, item, spider):
        # what = item_type(item)
        # if what in set(self.SaveTypes):
        # self.exporters[what].export_item(item)
        # if tracked or all, only include 13 products track list
        if item["model"] in set(self.tracked_prdcts):
            self.exporters[self.SaveTypes[0]].export_item(item)
        self.exporters[self.SaveTypes[1]].export_item(item)
        self.exporters[self.SaveTypes[2]].export_item(item)
        return item
