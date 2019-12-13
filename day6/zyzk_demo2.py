#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# Date: 2019/11/14 0014 19:08
# Author: Mijiu
# Version: 1.0
import json, requests, pymysql, chardet, sys, io, re
from pyquery import PyQuery as pq
from lxml import etree
lis_2_url = list()
lis_3_url = list()
lis_3_id = list()
list_2_title = list()
dic1 = list()
# 获取页面源码 (中医智库) by Rosny 2019-11-12
def Get_page(url):
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    data = requests.get(url, headers=header)
    return data.text

def Get_page2(list_hot_data):
    # global list_2_title  # 素问 ....
    global lis_3_url
    param = {
        'total': 97,
    }
    url = f'https://www.zk120.com/ji/search?qe={list_hot_data}&nav=ys'
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    result = requests.get(url, headers=header, params=param)

    intota = result.json()['total']  # 97
    data = result.json()
    lis1 = list() # 热门97本书
    for bo in data["books"]:
        # print(bo["title"], bo["author"], bo["comment"], bo["url"])
        lis_3_url.append(bo["url"])
        lis_3_id.append(bo["id"])
        title_ = bo["title"]
        title_ = title_.replace('<span class="highlight-kw">', ' ')
        title_= title_.replace('</span>', ' ')
        title_= title_.strip()
        lis1 .append(title_)


    s = 10
    e = 20
    if int(intota) <= 10:
        return lis1
    else:
        for i in range(int(intota / 10)+1):
            param = {
                'total': intota,
                's': s,
                'e': e,
            }
            s += 10
            e += 10
            url = f'https://www.zk120.com/ji/search?qe={list_hot_data}&nav=ys'
            result = requests.get(url, headers=header, params=param)
            books = result.json()["books"]
            if len(books) < 1:
                continue
            else:

                for bo in books:
                    # print(bo["title"],bo["author"],bo["comment"],bo["url"])
                    lis_3_url.append(bo["url"])
                    lis_3_id.append(bo["id"])
                    title = str(bo["title"])
                    title = title.replace('<span class="highlight-kw">',' ')
                    title = title.replace('</span>', ' ')
                    title = title.strip()

                    lis1.append(title)


            s += 10
            e += 10



        return lis1

# 获取第一页标题
def Get_data_1():
    global lis_2_url
    lis_hot_data = list()  # 黄帝内经 ....
    url = 'https://www.zk120.com/ji/group/?nav=ys'
    data = Get_page(url)
    html_1 = pq(data)
    h2 = html_1('section.ice_bg h2')
    ul = html_1('section.ice_bg ul')
    for p, q in zip(h2, ul):
        ul_1 = html_1(q)('li a')
        for a in ul_1:
            # print(html_1(p).text(),html_1(a).text(),'https://zk120.com'+html_1(a).attr('href'))
            lis_2_url.append('https://zk120.com' + html_1(a).attr('href'))
            lis_hot_data.append(html_1(a).text())

    return lis_hot_data


def Get_data_2():
    pass

# 获取第三页标题
def Get_data_3():

    data_mulu_list_all = list()  # 目录数据
    Nr_list = list()   # 内容数据
    # Zname = list()  # 作者
    for i in lis_3_url:   # 获取内容数据
        url = 'https://www.zk120.com'+ i
        data = Get_page(url)

        html_1 = pq(data)
        p = html_1('div.abstract_wrapper p')
        # name = html_1('div.book_info.pr p.book-author.share_description_config.baike_author')

        for j in p:
            Nr_list.append(html_1(j).text())

    for num in lis_3_id:  # 获取目录数据
        data_mulu = ''

        url = 'https://www.zk120.com/ji/catalog/'+f'{num}'
        __json = json.loads(Get_page(url))
        children_data = list()
        # print(__json["catalog"]["t"])
        # print(__json)
        data_mulu +=f'{__json["catalog"]["t"]},'
        for k in __json["catalog"]["children"]:
            if "children" in k.keys():
                for c in k["children"]:
                    try:
                        print(c["t"])
                    except Exception as E:
                        print("因为字符集错误删除一条数据!",E)
                    else:
                        data_mulu += f'{c["t"]},'

            else:
                try:
                    print(k["t"])
                except Exception as e:
                    print("因为字符集错误删除一条数据!",e)
                else:
                    data_mulu += f'{k["t"]},'
            # print(data_mulu)    # 目录完整内容
        data_mulu_list_all.append(data_mulu)



    return [Nr_list,data_mulu_list_all]
def test():

    data_title = Get_data_1()   # 标题 :6热门
    data_mulu_nr = Get_data_3()     # 目录和内容

    for i,ii in zip(data_title[:6],list_2_title):
        # print(list_2_title,data_mulu_nr[0],data_mulu_nr[1])
            for p,j,k in zip(ii,data_mulu_nr[0],data_mulu_nr[1]):
                print("-----")
                print(i)   # 热门标题
                print(p)    # 第二页title
                print(j)    # 热门内容
                print(k)    # 热门目录
    print("----")
    print(data_mulu_nr[0], len(data_mulu_nr[0]))
    print(data_mulu_nr[1], len(data_mulu_nr[1]))


# 建立数据库对象函数
def Mysql_obj(name,sql,lis):
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        passwd="mysql123",
        db=name,
        charset="utf8"
    )
    cursor = conn.cursor()
    cursor.execute(sql, lis)
    conn.commit()
    cursor.close()
    conn.close()
    print("数据存储成功!")

if __name__ == '__main__':
    list_hot_data = Get_data_1()[:6]  # ['黄帝内经', '本草纲目', '伤寒杂病论', '医宗金鉴', '景岳全书', '四圣心源']
    list_putng_data = list_hot_data[6:]

    for i in list_hot_data:
        tit = Get_page2(i)
        list_2_title.append(tit)

    # print(lis_3_url)

    # Get_data_2()
    # Get_data_3()
    test()


