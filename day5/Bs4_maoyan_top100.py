#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# Date: 2019/11/11 0011 20:32
# Author: Mijiu
# Version: 1.0
import requests,csv
from bs4 import BeautifulSoup


# 获取页面源码 (猫眼电影top100) by Rosny 2019-11-11
def Get_page(num=0):
    pr = {
        "offset":num*10
    }
    url = 'https://maoyan.com/board/4'

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"
    }
    response = requests.get(url,headers=header,params=pr)
    return response.text

# 分析数据 (Xpath验证) 顺手清理数据 by Rosny 2019-11-11
def Get_data(data):
    soup = BeautifulSoup(data,"lxml")
    MV = list()
    for i in soup.find_all('dd'):
        lis = list()
        for j in i.find_all('p'):
            lis.append(j.string)
        lis.append(i.find_all('i')[1].string + i.find_all('i')[2].string)
        for y in i.find_all(attrs={'class':'board-img'}):
            lis.append(y.attrs["data-src"])
        MV.append(lis)
        print(MV)
    return MV

# 数据清洗  by Rosny 2019-11-7
def Data_cleaning(data):
    num = list()
    for i in data:
        i.pop(3)
        for j in range(len(i)):
                i[j] = i[j].strip()

    return data


# CSV格式存储清洗过后的数据
def Csv_data(data):
    with open("bs4_maoyan_top100/top100.csv","a") as cf:
        wf = csv.writer(cf)
        wf.writerows(data)

# 获取图片
def Get_img():
    data = list()
    for i in range(10):
        for j in Data_cleaning(Get_data(Get_page(i))):
            response = requests.get(j[4])
            yield response.content

            # with open(f"bs4_maoyan_top100/img/{j[0]}.jpg", "wb") as f:
            #     f.write(response.content)

# 主函数
def main():

    for i in range(10):
        # Csv_data(Data_cleaning(Get_data(Get_page(i))))
        for j in Data_cleaning(Get_data(Get_page(i))):
            print(j)
    for i in Get_img():
        print(i)

if __name__ == '__main__':
    main()


