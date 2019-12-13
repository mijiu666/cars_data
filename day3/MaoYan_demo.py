#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# Date: 2019/11/7 0007 14:18
# Author: Mijiu
# Version: 1.0

import requests,re,csv

# 获取页面源码 (猫眼电影top100) by Rosny 2019-11-7
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

# 分析数据 (正则验证) by Rosny 2019-11-7
def Get_data(data):
    reobj = re.findall('<dd.*?title="(.*?)".*?data-src="(.*?)".*?star">(.*?)<.*?time">(.*?)<.*?ger">(.*?)<.*?tion">(\d)',data,re.S)
    return reobj

# 数据清洗  by Rosny 2019-11-7
def Data_cleaning(data):
    data_lis = list()
    for i in data:
        data_lis.append(list(i))
    for j in data_lis:
        j[2] = j[2].strip()
        j[4] = j[4]+j[5]
        j.pop()


    return data_lis

# CSV格式存储清洗过后的数据
def Csv_data(data):
    # for i in data:
    with open("file.csv","a+") as cf:
        wf = csv.writer(cf)
        wf.writerows(data)

# 获取图片
def Get_img():
    data = list()
    for i in range(10):
        for j in (Data_cleaning(Get_data(Get_page(i)))):
            data.append(j)
    num = 1
    for i in data:
        response = requests.get(i[1])
        print(i)
        # with open(f"img/{num}.jpg","wb") as f:
        #     f.write(response.content)
        num +=1

# 主函数
def main():
    for i in range(10):

        # Csv_data(Data_cleaning(Get_data(Get_page(i))))
        print(Get_data(Get_page(i)))




if __name__ == '__main__':

    main()
    # Get_img()

