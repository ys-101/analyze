"""
链家二手房示例,后续自己完善
"""
import math
import openpyxl
import requests
from lxml import etree
from fake_useragent import UserAgent
import pymysql
import time
import random

wb = openpyxl.Workbook()            # 创建工作簿
ws_lg = wb.active                # 获取工作表
ws_lg.title = "济南链家二手房数据"
ws_lg.append(['小区名字', '总价', '户型', '面积',
                 '单价', '朝向', '楼层',
                 '装饰','区域'])


# # MySQL
# db = pymysql.connect('localhost','root','123456','lianjiadb',charset='utf8')
# cur = db.cursor()
# ins = 'insert into lianjiatab values(%s,%s,%s,%s,%s)'


# 1.请求
# p:多少万
url = 'https://jn.lianjia.com/ershoufang/{}'

headers = {'User-Agent':UserAgent().random}

# 一页30 最多显示100页
dict_city = {0:'lixia',
             1:'shizhong',
             2:'tianqiao',
             3:'licheng',
             4:'huaiyin',
             5:'gaoxin',
             6:'jiyang',
             7:'shanghe',
             8:'pingyin',
             9:'zhangqiu1',
             10:'changqing'}

for sum in range(0,11):
    city = dict_city[sum]
    # print(now_url.format(city))
    html = requests.get(url=url.format(city), headers=headers).text
    # 2.解析
    eobj = etree.HTML(html)
    page = eobj.xpath('//h2[@class="total fl"]/span/text()')[0]
    # print(type(int(page)))
    if int(page) >3000:
        list_price = ['p1','p2','p3','p4','p5','p6']
        for price in list_price:
            one_url = 'https://jn.lianjia.com/ershoufang/{}/{}/'.format(city,price)
            print(one_url)
            one_html = requests.get(url=one_url, headers=headers).text
            one_eobj = etree.HTML(one_html)
            one_page = one_eobj.xpath('//h2[@class="total fl"]/span/text()')[0]
            # print(one_page)
            two_page = math.ceil(int(one_page) / 30)
            for p in range(1, two_page + 1):
                try:
                    two_url = 'https://jn.lianjia.com/ershoufang/{}/pg{}{}/'.format(city,p,price)
                    print(two_url)
                    two_html = requests.get(url=two_url, headers=headers).text
                    two_eobj = etree.HTML(two_html)
                    # 名
                    list_name = two_eobj.xpath('//div[@class="positionInfo"]/a[1]/text()')
                    # 总价
                    list_total = two_eobj.xpath('//div[@class="totalPrice"]/span/text()')
                    # 户型
                    list_type = two_eobj.xpath('//div[@class="houseInfo"]/text()')
                    # 建筑面积
                    list_area = two_eobj.xpath('//div[@class="houseInfo"]/text()')
                    # 单价
                    list_unprice = two_eobj.xpath('//div[@class="unitPrice"]/span/text()')
                    # 朝向
                    list_orientation = two_eobj.xpath('//div[@class="houseInfo"]/text()')
                    # 楼层
                    list_floor = two_eobj.xpath('//div[@class="houseInfo"]/text()')
                    # 装修
                    list_fitment = two_eobj.xpath('//div[@class="houseInfo"]/text()')
                    # 区域
                    list_region = two_eobj.xpath('//div[@class="positionInfo"]/a[2]/text()')

                    # 一条二手房信息
                    for i in range(0,len(list_name)):
                        message = []
                        message.append(list_name[i])
                        message.append(list_total[i])
                        message.append(list_type[i].split(' | ')[0])
                        # .split('平')[0]
                        area = list_area[i].split(' | ')[1]
                        message.append(area.split('平')[0])
                        money = list_unprice[i].split('元')[0]
                        message.append(money.split('价')[1])
                        message.append(list_orientation[i].split(' | ')[2])
                        message.append(list_floor[i].split(' | ')[4])
                        message.append(list_fitment[i].split(' | ')[3])
                        message.append(list_region[i])
                        # print(message)
                        ws_lg.append(message)
                        # 一会在这存储数据
                    time.sleep(random.uniform(3,5))
                    print("已存数据:",p * 30)
                except Exception as e:
                    print("错误类型:",e)
                    continue

    else:
        two_page = math.ceil(int(page) / 30)
        for p in range(1, two_page + 1):
            try:
                two_url = 'https://jn.lianjia.com/ershoufang/{}/pg{}/'.format(city, p)
                print(two_url)
                two_html = requests.get(url=two_url, headers=headers).text
                two_eobj = etree.HTML(two_html)
                # 名
                list_name = two_eobj.xpath('//div[@class="positionInfo"]/a[1]/text()')
                # 总价
                list_total = two_eobj.xpath('//div[@class="totalPrice"]/span/text()')
                # 户型
                list_type = two_eobj.xpath('//div[@class="houseInfo"]/text()')
                # 建筑面积
                list_area = two_eobj.xpath('//div[@class="houseInfo"]/text()')
                # 单价
                list_unprice = two_eobj.xpath('//div[@class="unitPrice"]/span/text()')
                # 朝向
                list_orientation = two_eobj.xpath('//div[@class="houseInfo"]/text()')
                # 楼层
                list_floor = two_eobj.xpath('//div[@class="houseInfo"]/text()')
                # 装修
                list_fitment = two_eobj.xpath('//div[@class="houseInfo"]/text()')
                # 区域
                list_region = two_eobj.xpath('//div[@class="positionInfo"]/a[2]/text()')

                # 一条二手房信息
                for i in range(0, len(list_name)):
                    message = []
                    message.append(list_name[i])
                    message.append(list_total[i])
                    message.append(list_type[i].split(' | ')[0])
                    message.append(list_area[i].split(' | ')[1])
                    message.append(list_unprice[i].split('元')[0])
                    message.append(list_orientation[i].split(' | ')[2])
                    message.append(list_floor[i].split(' | ')[4])
                    message.append(list_fitment[i].split(' | ')[3])
                    message.append(list_region[i])
                    # print(message)
                    ws_lg.append(message)
                    # 一会在这存储数据
                time.sleep(random.uniform(3, 4))
                print("已存数据:", p * 30)
            except Exception as e:
                print("错误类型:", e)
                continue

wb.save('secondhand_house1.xlsx')
    # 存入MySQL数据库


#     cur.execute(ins, L)
#     db.commit()
#
# cur.close()
# db.close()






















