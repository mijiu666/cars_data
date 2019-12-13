#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# Date: 2019/12/10 0010 12:51
# Author: Mijiu
# Version: 1.0
import json
import time
import pymysql
import requests


# 东方财富网
def getPage( number):
    '''
    对目标网站进行数据采集
    :param number: 采集多少页
    :return: 采集到的数据
    '''
    strUrl = 'http://33.push2.eastmoney.com/api/qt/clist/get'
    params = {
        'cb': 'jQuery1124011214511892561374_1575904469870',
        'pn': str(number),
        'pz': '20',
        'po': '1',
        'np': '1',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': '2',
        'invt': '2',
        'fid': 'f3',
        'fs': 'm:0 t:6,m:0 t:13,m:0 t:80,m:1 t:2,m:1 t:23',
        'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152',
        '_': '1575904469955'
    }
    response = requests.get(strUrl, params=params)

    # 处理多余数据方便转换为字典
    data = response.text.replace("jQuery1124011214511892561374_1575904469870",'').replace('(',"").replace(')','').replace(';','')

    return json.loads(data)

num_a = 0

def Get_Data(num):
    '''
    对东方财富网抓抓取的数据进行处理
    :return:
    '''
    global num_a
    for i in range(1, num):
        time.sleep(0.2)
        data = getPage(i)
        for t1 in data.get('data').get('diff'):

            num_a+=1
            print(num_a,t1)
            # print(num_a,t1.get('f12'),t1.get('f14'))
            # print(f'最新价: {t1.get("f2")}   成交量: {t1.get("f5")} ')
            sql = 'insert into STOCK values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
            list1 = [str(num_a),t1.get('f12'),t1.get('f14'),t1.get('f2'),t1.get('f4'),t1.get('f5'),t1.get('f6'),t1.get('f7'),t1.get('f8'),t1.get('f15'),t1.get('f16'),t1.get('f17'),t1.get('f18'),t1.get('f23')]
            Get_mysql(sql_ = sql,data = list1)
# f2最新价 f3涨跌幅 f4涨跌额 f5成交量 f6成交额 f7振幅  f8换手率 f12 代码  f14 名称  f15最高价  f16最低  f17今开 f18昨收  f23 市净率


def Get_mysql(sql_,data):
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        passwd="mysql123",
        db="stock",
        charset="utf8"
    )
    cursor = conn.cursor()
    sql = '''
    CREATE TABLE STOCK(
    id CHAR(15),
    代码 CHAR(20),
    stock_name CHAR(10) NOT NULL UNIQUE,
    最新价 CHAR(10),
    涨跌幅 CHAR(10),
    成交量 CHAR(20),
    成交额 CHAR(30),
    振幅 CHAR(20),
    换手率 CHAR(20),
    最高价 CHAR(20),
    最低价 CHAR(20),
    今开 CHAR(20),
    昨收 CHAR(20),
    市净率 CHAR(20)
    )ENGINE=innodb DEFAULT CHARSET=utf8 COLLATE=utf8_bin
    ;
    '''
    cursor.execute(sql_,data)
    conn.commit()
    cursor.close()
    conn.close()
    print("数据存储成功!")


if __name__ == '__main__':
    Get_Data(100)
    # Get_mysql("1","2")