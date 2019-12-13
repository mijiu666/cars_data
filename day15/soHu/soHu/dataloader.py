#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# Date: 2019/11/29 0029 15:37
# Author: Mijiu
# Version: 1.0
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,Join,Compose


class NewsLoader(ItemLoader):
    default_output_processor = TakeFirst()


class SohuLoader(NewsLoader):
    text_out = Compose(Join(),lambda s: s.strip())
    source_out = Compose(Join(),lambda s: s.strip())