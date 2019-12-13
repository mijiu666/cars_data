#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# Date: 2019/12/11 0011 15:00
# Author: Mijiu
# Version: 1.0
import json
import pymongo
import requests
import threading
from lxml import etree

url = 'https://price.pcauto.com.cn/api/hcs/select/compareNewBar/serial_brand_json_chooser?type=1'

def Get_page():
    '''
    太平洋汽车网源码抓取
    :return:
    '''
    all_car = {}  # 所有数据最大字典
    response = requests.get(url)
    all_cars_json = json.loads(response.text.replace(';','').replace('var listCompareInfo = ',''))
    for i in all_cars_json:

        print('品牌------------------------')
        print(i.get('ID'))
        print(i.get('NAME'))
        print(i.get('LETTER'))
        # print(i.get('LIST'))
        for i2 in i.get('LIST'):   # 厂商
            print('厂商 -------------------------')
            print(i2.get('ID'))
            print(i2.get('NAME'))
            # print(i2.get('LIST'))
            for i3 in i2.get('LIST'):
                print('车系 -----------------------------')
                print(i3.get('ID'))
                print(i3.get('NAME'))
                # Get_car_series(i3.get('ID'))
                #   获取车系内经销商
                t1 = threading.Thread(target=Get_car_series,args=(i3.get('ID'),i3.get('NAME')) )
                t1.start()
                # 获取车系所有参数  车款
                t2 = threading.Thread(target=Get_config, args=(i3.get('ID'),))
                t2.start()
                # Get_config(i3.get('ID'))
                # 获取车系的 所有用户评价
                t3 = threading.Thread(target=Get_Estimate, args=(i3.get('ID'),))
                t3.start()
                # 获取车款的详细配置参数
                t4 = threading.Thread(target=Get_config2, args=(i3.get('ID'),))
                t4.start()
                t1.join(timeout=100)
                t2.join(timeout=100)
                t3.join(timeout=100)
                t4.join(timeout=100)
        print('结束---------------')


def Get_car_series(CarId,CarName):
    '''
    获取车型 和参数 经销商
    :param CarId:  每个车系的网址参数
    :return:
    '''
    url = f'https://price.pcauto.com.cn/price/sg{CarId}/'
    try:
        response = requests.get(url)
        html = etree.HTML(response.text)
        # 经销商url
        JxsURL = 'https:' + html.xpath('//div[@class="navB-inner"]/ul/li[5]/a/@href')[0] + f'c353/sg{CarId}/'
        Get_Jxs(JxsURL,CarName)
    except:
        pass

    # 请求车型详细配置
    # config_id = html.xpath('//div[@class="tab-con clearfix"]//dl//p[@class="name"]/a/@href')
    # if len(config_id) > 0:
    #       # /m86697/
    #     # config_url = f'https://price.pcauto.com.cn/{config_id[0]}config.html'
    #     config_url = f'https://m.pcauto.com.cn/auto/sg{config_id[0]}/config.html'
    #     Get_config(config_url)

def Get_Jxs(JxsURL,CarName):
    """
    获取经销商信息
    :param JxsURL:  经销商页面url
    :return:
    """
    response = requests.get(JxsURL)
    html = etree.HTML(response.text)
    all_Jsx = {}
    all_Jsx[CarName] = {}
    if len(html.xpath('//div[@class="listTb"]/ul/li')) > 0:
        for i in html.xpath('//div[@class="listTb"]/ul/li'):

            fourS = i.xpath('.//p/span[@class="icon icon-jxs-gray"]/text()')  # 4S
            ZanShi = i.xpath('.//p/span[@class="icon icon-jxs-green"]/text()')  # 展示厅
            if len(fourS) > 0:
                JxsType = fourS[0]
            else:
                JxsType =ZanShi[0]
            all_Jsx[CarName][JxsType + " " + i.xpath('.//a/strong/text()')[0]] = {}  # 4s or  展示厅
            all_Jsx[CarName][JxsType + " " + i.xpath('.//a/strong/text()')[0]]['店名'] = i.xpath('.//a/strong/text()')[0]
            all_Jsx[CarName][JxsType + " " + i.xpath('.//a/strong/text()')[0]]['位置'] = i.xpath('.//span[@class="smoke"]/text()')[0] if len(i.xpath('.//span[@class="smoke"]/text()'))>0 else '暂无'
            all_Jsx[CarName][JxsType + " " + i.xpath('.//a/strong/text()')[0]]['电话'] = i.xpath('.//p[@class="tel"]/strong/text()')[0]
            all_Jsx[CarName][JxsType + " " + i.xpath('.//a/strong/text()')[0]]['主营品牌'] = i.xpath('.//p[@class="tel"][2]/span[2]/text()')[0]
            all_Jsx[CarName][JxsType + " " + i.xpath('.//a/strong/text()')[0]]['地址'] = i.xpath('.//p[@class="pFc"][1]/span[2]/text()')[0]
            # print(fourS[0] if len(fourS) > 0 else ZanShi[0])
            # print(i.xpath('.//a/strong/text()')[0])  # 店名
            # print(i.xpath('.//span[@class="smoke"]/text()')[0] if len(i.xpath('.//span[@class="smoke"]/text()'))>0 else '暂无')  # 位置
            # print(i.xpath('.//p[@class="tel"]/strong/text()')[0])  # 电话
            # print(i.xpath('.//p[@class="tel"][2]/span[2]/text()')[0])  # 主营品牌
            # print(i.xpath('.//p[@class="pFc"][1]/span[2]/text()')[0])  # 地址
    mongo('Jxs_all',all_Jsx)


def Get_config(Car_id):
    """
    请求车型参数
    :param url: 车型id    config.html
    :return:
    """
    url = f'https://price.pcauto.com.cn/api/hcs/select/compareNewBar/serial_recommend_model?sgid={Car_id}&mid=0&callback=jQueryUser_duibi_callback_yourlike'
    response = requests.get(url)

    config_dict = json.loads(response.text.replace('jQueryUser_duibi_callback_yourlike(', '').replace(')', ''))
    for i in config_dict.get('result').get('models'):
    # {'id': '93809', 'name': '奥迪A3 2020款 Sportback 35 TFSI 进取型', 'price': '18.92万', 'photo': '//img.pcauto.com.cn/images/upload/upc/tx/auto5/1901/12/c8/128021263_1547294360575_80x60.jpg', 'url': '//price.pcauto.com.cn/m93809/', 'sgId': '9550'}
        try:
            mongo('car_Kuan', i)   # 车款
        except Exception as e:
            with open('car_Kuan_error.txt','a+',encoding='utf-8') as f:
                f.write(e)
                f.write('\n')



def Get_config2(Car_id):
    """
    获取车型详情参数
    :param Car_id:
    :return:
    """
    all_car_dic = {}
    url = f'https://m.pcauto.com.cn/auto/sg{Car_id}/config.html'
    response = requests.get(url)
    config_html = etree.HTML(response.text)
    # 35种车型
    allCarName = [car_name.replace('.','-') for car_name in config_html.xpath('//div[@class="m-pnl"]//div[@class="m-type"]/p/span/text()')]

    title_list = [title for title in config_html.xpath('//div[@class="m-con-left"]/div/p/text()') if title != '\r\n']
    # car_data 参数内容

    for car_data in config_html.xpath('//*[@id="Jscroll"]/div/div'):
        allCarData = [car_data.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '●') for car_data
                      in car_data.xpath('.//p')]

        for name in allCarName:
            all_car_dic[name] = {}
            for tit, data in zip(title_list, allCarData):
                a = {tit.replace('.','-'):data}
                all_car_dic[name].update(a)
                # print(f"{tit} :{data}")
    mongo('all_cars',all_car_dic)


def Get_Estimate(Carid):
    """
    获取各个车型用户评价
    :param Carid:
    :return:
    """

    url = f'https://price.pcauto.com.cn/comment/interface/auto/serial/serial_group_comments_json.jsp?sgid={Carid}&pageNo=1&zj=&type=1&hasStick=1&callback=jsonp1'
    # response = requests.get(url)
    try:
        response = requests.get(url)
        estimate_page = json.loads(response.text.replace('jsonp1(','').replace(')','')).get('pageCount')
    except:
        pass
    else:
        num1 = 0
        if estimate_page is None or int(estimate_page) < 2:
            print("该车系暂无评价")
        else:
            for num in range(2, int(estimate_page)):
                url = f'https://price.pcauto.com.cn/comment/interface/auto/serial/serial_group_comments_json.jsp?sgid={Carid}&pageNo={num}&zj=&type=1&hasStick=1&callback=jsonp{num + 3}'
                # url = f'https://price.pcauto.com.cn/comment/interface/auto/serial/serial_group_comments_json.jsp?sgid=9550&pageNo=1&zj=&type=1&hasStick=1&callback=jsonp1'

                response1 = requests.get(url)
                # 用户评价
                try:
                    estimate_json = json.loads(response1.text.replace(f'jsonp{num + 3}(', '').replace(')', ''))
                # print(estimate_json)
                except:
                    print("评价查询结束!")
                    break

                for user in estimate_json.get('result'):
                    # try:
                    num1 += 1
                    mongo('Estimate',user)

                    # print(user.get('createTime'))  # 评价时间
                    # print(user.get('averageScore'))  # 评分
                    # print(user.get('regionName'))
                    # print(num1, user.get('nickName').replace('\ufffd', ''))  # 用户名
                    # print(user.get('modelName'))  # 购买车型
                    # print(user.get('price'), '万')  # 裸车价
                    # print(user.get('content'))  # 评语
                    # print('-------------------')


def mongo(tableName,data):
    """
    mongoDB数据库存储
    :param tableName:   表名
    :param data:  数据
    :return:
    """
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.cars_family
    collection = db[tableName]
    result = collection.insert(data)
    print(f"{tableName}全部数据储存成功!")

if __name__ == '__main__':

    Get_page()