# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

num = 0
class SohuPipeline(object):
    def process_item(self, item, spider):
        global num
        num +=1
        file = r'news\\' + str(num) + '.text'
        with open(file,'a',encoding='utf-8') as f:
            f.write(item['title'] + '\n')
            f.write(item['text'] + '\n')
        return item
