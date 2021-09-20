import pymysql
import requests
from datetime import datetime
from settings import SERVICE_ENDPOINT, SERVICE_SECRET


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
    cursor, db = open_database()
    keys = ', '.join(new_data.keys())
    values = ', '.join(['%s'] * len(new_data))
    check_sql = "INSERT INTO {kind}({keys}) VALUES ({values});".format(kind=kind, keys=keys, values=values)
    print(check_sql)
    try:
        if cursor.execute(check_sql, tuple(new_data.values())):
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
    cursor, db = open_database()
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    print(data)
    check_sql = "INSERT INTO {kind}({keys}) VALUES ({values});".format(kind=kind, keys=keys, values=values)
    print(check_sql)
    try:
        if cursor.execute(check_sql, tuple(data.values())):
            print('Successful')
            db.commit()
    except:
        print('Failed')
        db.rollback()
    db.close()


def check_exit(kind, data, exit_num):
    """ 检验数据是否存在

    :param kind: 数据属于哪一类
    :param data: 待检查数据
    :param exit_num: 仅给review使用,用于判断已有的评论数
    :returns 0-20: 数据库中所含的重复数据（2-20仅供reviews使用）
    :returns r_check： 返回的已经存在数据库中的数据

    """
    if kind == 'shopreviews':
        user_id = data['user_id']
        cursor, db = open_database()
        if user_id == '0':
            check_sql = "SELECT * FROM shopreviews WHERE review_hash = %s AND shop_id = %s AND user_id = %s;"
            print(check_sql)
            cursor.execute(check_sql, (data['review_hash'], data['shop_id'], 0))
            result = cursor.fetchone()
            if result:
                print('We already have this review!!!')
                db.close()
                return exit_num + 1, result

        else:
            check_sql = "SELECT * FROM shopreviews WHERE review_hash = %s AND shop_id = %s AND user_id = %s AND review_time = %s;"
            print(check_sql)
            cursor.execute(check_sql,
                           (data['review_hash'], data['shop_id'], data['user_id'], data['review_time']))
            result = cursor.fetchone()
            if result:
                print('We already have this review!!!')
                db.close()
                return exit_num + 1, result
    else:
        cursor, db = open_database()
        check_sql = "SELECT id FROM shopdetails WHERE shop_id = %s;"
        print(check_sql)
        shop_id = data['shop_id']
        if cursor.execute(check_sql, (shop_id,)):
            result = cursor.fetchone()
            db.close()
            return 1, result
    db.close()
    return 0, None


def get_saved_reviews(kind, shop_id):
    """ 为shopReviews和shopMains获取各个店铺已存评论

    :param kind: 列表种类
    :param shop_id: 店铺
    :returns response['totalRecords']: 所有已存评论
    :returns re_shopmain['id']: 店铺在shopMains数据库中的id


    """
    cursor, db = open_database()
    sql_1 = "SELECT COUNT(*) FROM shopreviews WHERE shop_id = %s;"
    sql_2 = "SELECT id,COUNT(*) FROM shopmains WHERE new_shop_id = %s;"
    # 对shopMains而言只能查new_shop_id
    # 暂时为新创建的shopMains使用,后面必须改
    if kind == 'shopmains':
        cursor.execute(sql_2, (shop_id, ))
        row = cursor.fetchone()
        return row[0], row[1]
    else:
        print(sql_1)
        cursor.execute(sql_1, (shop_id, ))
        row = cursor.fetchone()
        return row[0], shop_id


def update_saved_reviews(num, url_id):
    cursor, db = open_database()
    sql = "UPDATE shopmains SET saved_reviews = %s WHERE new_shop_id = %s;"
    print(sql)
    try:
        cursor.execute(sql, (num, url_id, ))
        db.commit()
        print('Saved reviews have been updated!')
    except:
        print('Failed')
        db.rollback()
    db.close()
