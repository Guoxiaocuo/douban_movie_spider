# 爬取豆瓣上某些条件下能显示出来的所有影片信息【豆瓣能显示出来10000个】
# 目前程序设置的是爬取【形式为“电影”+评分在0-10之间+按照“近期热门”排序】三个条件下的影片
import random
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
allinfo=[]
# 这里urls的基本形式可以根据所要爬取内容需求来更改，例如：range=0,10代表豆瓣评分在0-10之间，若想爬取高分电影信息，可更改range范围
# 但要注意此处urls并不是浏览器中看到的url，需要根据页面源代码找到真正的url形式【获取真正url形式以及对其形式的拆分解释见使用说明】
# 此处range(参数1,参数2,参数3)也可任意修改。参数1：开始值（包括）；参数2：结束值（不包括）；参数3：每隔几个取一次
# 在豆瓣中一个页面一般有20个影片，所以参数3固定为20；参数1和参数2可调整，但差值要是20的倍数
urls = ['https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={}'.format(number) for number in range(0,5000,20)]
result_data_list = []
for url in urls[:]:
    print('正在爬取' + url)
    res = requests.get(url,headers={'User-Agent': random.choice(User_Agents)})
    # print(res.text)
    if res:result_data_list.append([item['url'] for item in json.loads(res.text)['data']])
    seconds = random.uniform(4, 5)
    time.sleep(seconds)
#print(result_data_list)

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
    df.to_excel('douban_test.xlsx', sheet_name='Sheet1')
# 上面一行中有存入Excel的名称，可任意修改，文件路径是项目文件下
# 注：若项目文件中已有该名称的Excel文件，会自动覆盖，若不想被覆盖，需更改文件名或另存原文件
for i in range(0,len(urls)):
    utrl_list = result_data_list[i]
    for single_url in utrl_list:
        print(single_url)
        getinfo(single_url)
        seconds = random.uniform(3, 4)
        time.sleep(seconds)
        #此处time.sleep函数用来控制访问时间间隔，为防止爬取大量信息时访问频率过快触发反爬
    i+=1