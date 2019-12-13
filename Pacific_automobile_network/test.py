#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# Date: 2019/12/11 0011 16:25
# Author: Mijiu
# Version: 1.0
import json
import requests
from lxml import etree

# url = 'https://price.pcauto.com.cn/api/hcs/select/compareNewBar/serial_recommend_model?sgid=9550&mid=0&callback=jQueryUser_duibi_callback_yourlike'

# url = 'https://m.pcauto.com.cn/auto/comment/sg9550/'
url = f'https://price.pcauto.com.cn/comment/interface/auto/serial/serial_group_comments_json.jsp?sgid=9550&pageNo=1&zj=&type=1&hasStick=1&callback=jsonp1'
response = requests.get(url)
estimate_page = json.loads(response.text.replace('jsonp1(','').replace(')','')).get('pageCount')
num1 = 0
if estimate_page is None or int(estimate_page) < 2:
    print("该车系暂无评价")
else:
    for num in range(2,int(estimate_page)):
        url = f'https://price.pcauto.com.cn/comment/interface/auto/serial/serial_group_comments_json.jsp?sgid=9550&pageNo={num}&zj=&type=1&hasStick=1&callback=jsonp{num+3}'
        # url = f'https://price.pcauto.com.cn/comment/interface/auto/serial/serial_group_comments_json.jsp?sgid=9550&pageNo=1&zj=&type=1&hasStick=1&callback=jsonp1'

        response1 = requests.get(url)
        # 用户评价
        try:
            estimate_json = json.loads(response1.text.replace(f'jsonp{num+3}(','').replace(')',''))
        # print(estimate_json)
        except:
            print("评价查询结束!")
            break

        for user in estimate_json.get('result'):
            # try:
            num1 +=1
            with open('car_user.txt','a+',encoding='utf-8') as f:
                f.write(str(user))
                f.write('\n')

            print(user.get('createTime')) # 评价时间
            print(user.get('averageScore')) # 评分
            print(user.get('regionName'))
            print(num1,user.get('nickName').replace('\ufffd',''))   # 用户名
            print(user.get('modelName'))   # 购买车型
            print(user.get('price'),'万')  # 裸车价
            print(user.get('content'))    # 评语
            print('-------------------')
        # except Exception as e:
        # print('查找评价完毕!')
        #     print(e)
            # break






# url = 'https://m.pcauto.com.cn/auto/sg9550/config.html'
# # 35种车型
# allCarName = [car_name for car_name in config_html.xpath('//div[@class="m-pnl"]//div[@class="m-type"]/p/span/text()')]
# # for i in config_html.xpath('//div[@class="m-pnl"]//div[@class="m-type"]/p/span/text()'):
# #     print(i)
# title_list = [title for title in config_html.xpath('//div[@class="m-con-left"]/div/p/text()') if title != '\r\n']
# # car_data 参数内容
# for car_data in config_html.xpath('//*[@id="Jscroll"]/div/div'):
#     allCarData = [car_data.xpath('string(.)').replace('\r','').replace('\n','').replace('\xa0','●') for car_data in car_data.xpath('.//p')]
#
#     for name in allCarName:
#         print(name)
#         for tit,data in zip(title_list,allCarData):
#             print(f"{tit} :{data}")
# config_dict = json.loads(response.text.replace('jQueryUser_duibi_callback_yourlike(','').replace(')',''))
# print(type(config_dict))
# for i in config_dict.get('result').get('models'):
# # {'id': '93809', 'name': '奥迪A3 2020款 Sportback 35 TFSI 进取型', 'price': '18.92万', 'photo': '//img.pcauto.com.cn/images/upload/upc/tx/auto5/1901/12/c8/128021263_1547294360575_80x60.jpg', 'url': '//price.pcauto.com.cn/m93809/', 'sgId': '9550'}
#     print(i)
# # 车型参数
# config_id = html.xpath('//div[@class="tab-con clearfix"]//dl//p[@class="name"]/a/@href') # /m86697/
# config_url = f'https://price.pcauto.com.cn/{config_id}config.html'




# html.xpath('//div[@class="tab-con clearfix"]/div[@class="con"]//p[@class="name"]/a/@href')
# if html.xpath('//div[@class="listTb"]/ul/li') > 0:
#     for i in html.xpath('//div[@class="listTb"]/ul/li'):
#         fourS = i.xpath('.//p/span[@class="icon icon-jxs-gray"]/text()')     # 4S
#         ZanShi = i.xpath('.//p/span[@class="icon icon-jxs-green"]/text()')   # 展示厅
#         #
#         print(fourS[0] if len(fourS)>0 else ZanShi[0])
#         print(i.xpath('.//a/strong/text()')[0])   # 店名
#         print(i.xpath('.//span[@class="smoke"]/text()')[0])  # 位置
#         print(i.xpath('.//p[@class="tel"]/strong/text()')[0])  # 电话
#         print(i.xpath('.//p[@class="tel"][2]/span[2]/text()')[0]) # 主营品牌
#         print(i.xpath('.//p[@class="pFc"][1]/span[2]/text()')[0])  # 地址
