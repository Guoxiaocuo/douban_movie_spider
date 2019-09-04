# 已知豆瓣ID时，爬取影片信息
# 把已知的豆瓣ID存到项目文件中的'dubanIDs.xlsx'文件中即可，程序运行时自动导入该文件
# 此处仅以五个影片为例，在doubanID.xlsx文件中存了五个豆瓣ID
import random
import numpy as np
from bs4 import BeautifulSoup #解析包
import requests #请求包
import pandas as pd
import json
import time # 设置休眠时间，控制爬虫频率
from threading import Thread   # 多线程  爬虫比较多

User_Agents =[
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
]

doubanIDs_dataframe = pd.read_excel('doubanIDs.xlsx')
doubanID_array = np.array(doubanIDs_dataframe)
doubanID_list = doubanID_array.tolist()
print(doubanID_list)
doubanIDs=[]
for i in range(0,len(doubanID_list)):
    doubanID = doubanID_list[i]
    ID = doubanID[0]
    doubanIDs.append(ID)
print(doubanIDs)
urls = []
for doubanID in doubanIDs:
    url = 'https://movie.douban.com/subject/'+ str(doubanID)
    urls.append(url)
print(urls)

allinfo=[]
def getinfo(url):
    wdata = requests.get(url, headers={'User-Agent': random.choice(User_Agents)})
    wsoup = BeautifulSoup(wdata.text, 'lxml')
    names = wsoup.select('#content > h1 > span:nth-child(1)')
    info_all = wsoup.select('#info')
    data_one = info_all[0].get_text() if info_all else ""
    data_two = data_one.split('\n')
    directors = data_two[1].strip('导演: ') if len(data_two)>1 else ""
    actors = data_two[3].strip('主演: ') if len(data_two)>3 else ""
    types = data_two[4].strip('类型: ') if len(data_two)>4 else ""
    regions = data_two[5].strip('制片国家/地区: ') if len(data_two)>5 else ""
    reltimes = data_two[7].strip('上映日期: ') if len(data_two)>7 else ""
    secnames = data_two[9].strip('又名: ') if len(data_two)>9 else ""
    doubanscores = wsoup.select('#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > strong')
    sconumbers = wsoup.select('#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > div > div.rating_sum > a > span')
    introductions = wsoup.select('#link-report > span')
    info = {
        'url': url,
        'name': names[0].get_text() if names else "",
        'director':directors if directors else "",
        'actor':actors if actors else "",
        'type':types if types else "",
        'region':regions if regions else "",
        'reltime':reltimes if reltimes else "",
        'secname':secnames if secnames else "",
        'doubanscore': doubanscores[0].get_text() if doubanscores else "",
        'sconumber': sconumbers[0].get_text() if sconumbers else "",
        'introduction': introductions[0].get_text().strip() if introductions else ""

    }
    allinfo.append(info)
    df = pd.DataFrame(allinfo)
    df.to_excel('douban_IDtest.xlsx', sheet_name='Sheet1')
# 上面一行中有爬取下来的影片信息存入的Excel的名称，可任意修改，文件路径是项目文件下
# 注：若项目文件中已有该名称的Excel文件，会自动覆盖，若不想被覆盖，需更改文件名或另存原文件
for single_url in urls:
    print(single_url)
    getinfo(single_url)
    seconds = random.uniform(3,4)
    time.sleep(seconds)
