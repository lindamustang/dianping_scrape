import re
import requests
from pyquery import PyQuery as pq
from index_post_data import post_data, check_exit, update_data
from shopMains_num import get_shopMains_num


def shopMains(html):
    """ 处理大众点评点评索引页面数据，构建shopMain字典

    :param html: mitmproxy拦截下的大众点评网页源代码

    """
    review_num = get_shopMains_num(html)
    doc = pq(html)
    re_address = re.compile('data-address="(.*?)"')
    shops = doc('div.content>div#shop-all-list>ul>li').items()
    for i, shop in enumerate(shops):
        address_html = str(shop('div.operate.J_operate.Hide'))
        index_dict = dict()
        index_dict["shop_name"] = shop('div.txt>div.tit>a').attr('title').replace('&', '#')
        index_dict["new_shop_id"] = shop('div.txt>div.tit>a').attr('data-shopid')
        index_dict['trade_state'] = shop('span.istopTrade').text()
        if not index_dict['trade_state']:
            index_dict['trade_state'] = 'None'
        index_dict['address'] = re.findall(re_address, address_html)[0].replace('&', '#')
        index_dict['advertisement'] = 0
        if shop('div.tit>a.search-ad').text():
            index_dict['advertisement'] = 1
        index_dict['tuan_service'] = 0
        if shop("a.igroup"):
            index_dict['tuan_service'] = 1
        index_dict['wai_service'] = 0
        if shop("a.iout.icon-only"):
            index_dict['wai_service'] = 1
        index_dict['cu_service'] = 0
        if shop('a.ipromote'):
            index_dict['cu_service'] = 1
        index_dict['reviews'] = int(review_num[i])
        # index_dict['saved_reviews'] = get_saved_reviews('shopMains', index_dict["new_shop_id"])
        err_num = 0
        check_err_num = process_index_error(index_dict, err_num)
        if check_err_num == 1:
            continue


def process_index_error(index_dict, error_num):
    error_num += 1
    try:
        check_exit_num, r_check = check_exit('shopMains', index_dict)
        if check_exit_num == 0:
            post_data('shopmains', index_dict)
        else:
            update_data('shopmains', index_dict)

    except requests.exceptions.BaseHTTPError:
        if error_num < 3:
            process_index_error(index_dict, error_num)
        else:
            return 1
    return 0

