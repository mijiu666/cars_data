#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# Date: 2019/11/19 0019 15:27
# Author: Mijiu
# Version: 1.0
import pymysql
import pymongo
from day6.zyzk_demo2 import Mysql_obj
import requests,json
# pymysql 连接mysql模块
# pymongo 连接mango模块
# from day6.zyzk_demo2 import Mysql_obj   调用之前写好的 数据库储存函数
# requests 请求   json 转化数据格式

url = 'http://www.hebzhiyuan.com/api/colleges'
ur2 = 'http://www.hebzhiyuan.com/api/majors'

# 获取目标页面源码 by Rosny 2019-11-21
def Get_page(url,ma_x):
    for i in range(1,ma_x):
        data = {
            'parameters': {},
            '_pager': {'size': 15, 'page': i}
        }
        header = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Authorization":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1Ijoie1wiaWRcIjpcIjEwOTI0MjkwNjI2NDlcIixcInNjb3Jlc1wiOjU3MC4wLFwid2NcIjozMzAyOSxcImtsXCI6XCJCXCIsXCJwY1wiOlwiM1wiLFwic3RhcnRUc1wiOlwiMjAxOS0xMS0yMVQwOTo1Mjo0MS43NjQyNDk5KzA4OjAwXCIsXCJ0c1wiOjUzNS4yMTk2OTY3NzQwMTA1NyxcInBob25lXCI6XCJcIixcImRWYWx1ZVwiOjY4LjAsXCJyXCI6XCJSXCJ9In0.2nNvQ8zGjvBV2D7F_AjOBEysluksuXtozRi-r-Lcxd0",
            "Host": "www.hebzhiyuan.com",
            "Origin": "http://www.hebzhiyuan.com",
            "Referer": "http://www.hebzhiyuan.com /",
            "Connection":"keep-alive",
            "Content-Type": "application/json",
            "Content-Length": "47",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0"
        }
        response = requests.post(url,headers=header,data=json.dumps(data))
        yield response.text


#　获取对总数据进行清洗　　（页面１）
def Get_data(data):
    # data = Get_page()
    data = json.loads(data)[1]
    # print(data)
    for i in data["items"]:
        # print(i)   # 学校列表  ['19614', '电子科技大学(沙河校区)', 51, '028-61831137', True, True, '1']
        # print(i)
        # My_sql(i)
        Get_data_two()

        yield i[0]

def Get_page_two(i):   # 请求学校详情页　　（页面二）

    url = 'http://www.hebzhiyuan.com/api/colleges/info/' + str(i)
    header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1Ijoie1wiaWRcIjpcIjEwOTI0MjkwNjI2NDlcIixcInNjb3Jlc1wiOjU3MC4wLFwid2NcIjozMzAyOSxcImtsXCI6XCJCXCIsXCJwY1wiOlwiM1wiLFwic3RhcnRUc1wiOlwiMjAxOS0xMS0yMVQxNDo1Njo1OS43Nzg2MDEyKzA4OjAwXCIsXCJ0c1wiOjYxNy43OTYzNDczMTIxODc0NCxcInBob25lXCI6XCJcIixcImRWYWx1ZVwiOjY4LjAsXCJyXCI6XCJSXCJ9In0.LZuI44QX8d2GqLCd0wH8r5k9l04njoWCMCU0Ll-t_O0",
        "Host": "www.hebzhiyuan.com",
        "Origin": "http://www.hebzhiyuan.com",
        "Referer": "http://www.hebzhiyuan.com/",
        "Connection": "keep-alive",
        "Content-Length": "0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"
    }

    response = requests.post(url, headers=header,)

    yield json.loads(response.text)

# 对学校详情页面获取接收
def Get_data_two():
    for i in Get_page(url=url, ma_x=72):
        for j in Get_data(i):
            for k in Get_page_two(j):

                # k[key]=value  # 学校详细信息
                yield k


def Get_major():    # 获取专业信息
    for i in Get_page(url=ur2,ma_x=35):
        for j in json.loads(i)[1]['items']:
            lis1 = list()
            print(j)
            for k,y in j.items():
                lis1.append(y)


            yield lis1


# mysql 存储学校信息
def My_sql(data):

    sql = 'insert into school_data values(%s,%s,%s,%s,%s,%s,%s,%s,%s);'

    Mysql_obj(name='school_db',sql=sql,lis=data)
    print("成功!")



# 对学校详情页面总数据进行清洗
def Processing_data():

    for i in Get_data_two():
        lis1 = list()

        # print(i[1]["yxdm"])   # 编号
        # print(i[1]["yxmc"])  # 学校名称
        # print(i[1]["yxdz"])  # 所在地
        # print(i[1]["kszxdh"])  # 招生电话
        # print(i[1]["zgmc"])  # 主管部门
        # print(i[1]["yxbz"])  # 备注
        # print(i[1]["yxjblxdm"])  # 性质
        # print(i[1]["sf211"]) # 211
        # print(i[1]["sf985"]) # 985
        lis1.append(i[1]["yxdm"])
        lis1.append(i[1]["yxmc"])
        lis1.append(i[1]["yxdz"])
        lis1.append(i[1]["kszxdh"])
        lis1.append(i[1]["zgmc"])
        lis1.append(i[1]["yxbz"])
        lis1.append(i[1]["yxjblxdm"])
        lis1.append(i[1]["sf985"])
        lis1.append(i[1]["sf211"])
        yield lis1







# mango 存储专业信息
def mango_db(data):
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.school
    collection = db.school_test
    result1 = collection.insert_one(data)
    print("存储成功")

if __name__ == '__main__':
    # for i in Get_page(url=url,ma_x=72):
    #     for j in Get_data(i):
    #         for k in Get_page_two(j):
    #             print(k.items)# 学校详细信息
    #
    # for i in Get_data_two():
    #     print(i[1])


    # for i in Get_major():
    #     print(i)


    # print([i for i in Get_page_two(10001)])

    # try:
    #
    #     for i in Processing_data():
    #         # print(len(i))
    #         My_sql(i)
    # except Exception as e:
    #     print(e)
    #
    # print("存储完毕!")

    # for i in Get_page(url=ur2, ma_x=35):
    #     for j in json.loads(i)[1]['items']:
    #         mango_db(j)


    print("你好棒")