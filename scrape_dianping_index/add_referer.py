import re


def review_pages_referer(text, shop_id):
    """ referer生成

    :param text: review_all和review_all/p的结合
    :param shop_id: 店铺id
    :returns referer_url: 为目前url页数的前一页

    """

    if '/p' in text:
        re_page_num = re.compile('/review_all/p(.*)')
        page_num = re_page_num.findall(text)[0]
        page_num = int(page_num)
        if page_num != 1:
            referer_url = 'http://www.dianping.com/shop/' + shop_id + '/review_all/p' + str(page_num - 1)

        else:
            referer_url = 'http://www.dianping.com/shop/' + shop_id
    else:
        referer_url = 'http://www.dianping.com/shop/' + shop_id
    return referer_url


def shop_detail_referer(shop_id):
    referer_url = 'http://www.dianping.com/shop/' + shop_id + '/review_all'
    return referer_url


def shop_index_referer(index_url):
    re_index = re.compile('shanghai/ch10/(.*)')
    index_part = re_index.findall(index_url)[0]
    if 'cpt=' in index_part:
        re_page_num = re.compile('p(.*?)\?cpt=')
        cpt_page_num = re_page_num.findall(index_part)[0]
        page_num = int(cpt_page_num)
        index_url = index_url[:index_url.rfind('?') + 1]
        referer_url = index_url[:index_url.rfind('p') + 1] + str(page_num - 1)
    else:
        if 'p' not in index_part:
            referer_url = 'http://www.dianping.com/'
        else:
            re_page_num = re.compile('p(.*)')
            page_num = re_page_num.findall(index_part)[0]
            page_num = int(page_num)
            if page_num == 2:
                referer_url = index_url[:index_url.rfind('p')]
            elif page_num == 1:
                referer_url = 'http://www.dianping.com/'
            else:
                referer_url = index_url[:index_url.rfind('p') + 1] + str(page_num - 1)

    print(referer_url)
    return referer_url