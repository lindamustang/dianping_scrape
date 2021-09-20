import datetime
import pymysql
import csv
import random
import requests

# proxy_url = 'http://ip.16yun.cn:817/myip/pl/d81a7b16-e32e-410f-a144-e1d9a93631b3/?s=jsnfgdaups&u=txl1208&format=json'
# proxy_json = requests.get(proxy_url).json()
# print(proxy_json)
# proxy_port = (proxy_json['proxy'][0]['ip'], proxy_json['proxy'][0]['port'])
# print(proxy_port)
# db = pymysql.connect(host='localhost', passwd='1111', user='root', port=3306)
# cursor = db.cursor()
# cursor.execute('USE dianping;')
# sql_1 = "SELECT new_shop_id FROM shopmains WHERE reviews > 1000 AND type = '本帮江浙菜'; "
# # with open('shop_id.txt', 'r', encoding='utf-8', newline='') as f:
# #     shop_ids = f.readlines()
# shop_list = []
# cursor.execute(sql_1)
# row = cursor.fetchone()
# while row:
#     if row[0] is not None:
#         shop_list.append(row[0] + '\n')
#     row = cursor.fetchone()
# print(len(shop_list))
# # shop_list = shop_list + shop_ids
# # random.shuffle(shop_list)
# # with open('random_shop_id.txt', 'w', encoding='utf-8') as f1:
# #     for i in shop_list:
# #         f1.write(i)
# # shops = []
# # for i in shop_ids:
# #     shop_id = i.replace('\n', '')
# #     cursor.execute(sql_1, (shop_id,))
# #     row = cursor.fetchone()
# #     print(row)
# #     while row:
# #         if row[0] > 0:
# #             shops.append(shop_id)
# #         row = cursor.fetchone()
#
# # with open('last_100_shop_id.txt', 'w', encoding='utf-8') as f:
# #     for s in shops:
# #         f.write(s)
# #         f.writelines('\n')

#
with open('random_shop_id.txt', 'r', encoding='utf-8') as f:
    d = f.readlines()

for n, i in enumerate(d):
    if 'GaqYaC8nhuh8RoFy' in i:
        print(n)
#
#
# http://www.dianping.com/shop/G9ZRgxF2FhI9agDx/review_all/p31
#
# # csvFile = open('reviews.csv', 'w')
# # writer = csv.writer(csvFile)
# # writer.writerows(review_list)
#
# db.close()
#
# # db = pymysql.connect(host='localhost', passwd='1111', user='root', port=3306)
# # cursor = db.cursor()
# # cursor.execute('USE dianping;')
# # sql_1 = "SELECT COUNT(*) FROM shopreviews WHERE review_time REGEXP '2020-02' AND shop_id = %s;"
# # with open('aim_shop_min.txt', 'r', encoding='utf-8', newline='') as f:
# #     shop_ids = f.readlines()
# # shop_list = []
# # cursor.execute(sql_1)
# # row = cursor.fetchone()
# # while row:
# #     if row is not None:
# #         shop_list.append(row[1])
# #     row = cursor.fetchone()
#
# # for i in shop_ids:
# #     i = i.replace('\n', '')
# #     cursor.execute(sql_1, (i,))
# #     row = cursor.fetchone()
# #     # print(row)
# #     if row[0] == 0:
# #         shop_list.append(i)
# #
# # with open('aim_shop_true.txt', 'w', encoding='utf-8', newline='') as f:
# #     for i in shop_list:
# #         f.write(i)
# #         f.write('\n')
# #
#
# # csvFile = open('reviews.csv', 'w')
# # writer = csv.writer(csvFile)
# # writer.writerows(review_list)
#
# # db.close()
#
#
#
