import pymysql
import requests
from datetime import datetime


def open_database():
    db = pymysql.connect(host='localhost', passwd='1111', user='root', port=3306)
    cursor = db.cursor()
    cursor.execute('USE dianping;')
    return cursor, db


def update_data(kind, new_data):

    """ 更新数据函数

    :param kind: 数据属于哪一类
    :param new_data: 网页中提取的新数据

    """

    now = datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")
    new_data['updatedAt'] = date
    new_data['type'] = '本帮江浙菜'
    cursor, db = open_database()
    key_str = ''
    for key in new_data:
        key_str += str(key)
        key_str += '= %s, '
    update_sql = "UPDATE shopmains SET " + key_str[:-2] + " WHERE new_shop_id = " + '"' + new_data['new_shop_id'] + '";'
    print(update_sql)
    try:
        if cursor.execute(update_sql, tuple(new_data.values())):
            print('Successful')
            db.commit()
    except:
        print('Failed')
        db.rollback()
    db.close()


def post_data(kind, data):
    """ 提交各类数据

    :param kind: 数据库列表类型
    :param data: 提交数据


    """
    now = datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")
    data['createdAt'] = date
    data['updatedAt'] = date
    data['type'] = '本帮江浙菜'
    cursor, db = open_database()
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    print(data)
    post_sql = "INSERT INTO {kind}({keys}) VALUES ({values});".format(kind=kind, keys=keys, values=values)
    print(post_sql)
    try:
        if cursor.execute(post_sql, tuple(data.values())):
            print('Successful')
            db.commit()
    except:
        print('Failed')
        db.rollback()
    db.close()


def check_exit(kind, data):
    """ 检验数据是否存在

    :param kind: 数据属于哪一类
    :param data: 待检查数据
    :param exit_num: 仅给review使用,用于判断已有的评论数
    :returns 0-20: 数据库中所含的重复数据（2-20仅供reviews使用）
    :returns r_check： 返回的已经存在数据库中的数据

    """

    cursor, db = open_database()
    check_sql = "SELECT id FROM shopmains WHERE new_shop_id = %s;"
    print(check_sql)
    shop_id = data['new_shop_id']
    if cursor.execute(check_sql, (shop_id,)):
        result = cursor.fetchone()
        db.close()
        return 1, result

    db.close()
    return 0, None

# new_data = {'shop_name': '王小菜(洛平菜市场门店)', 'new_shop_id': 'layxGj2C74H0oG3u', 'type': '本帮江浙菜'}
# print(new_data.values())


# key_str = ''
# for key in new_data:
#     key_str += str(key)
#     key_str += '= %s, '
#
# print(key_str[: -2])