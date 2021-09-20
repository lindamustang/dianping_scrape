import re
import requests
from pyquery import PyQuery as pq
from resolve_1 import get_svg_dict1, str_combine_1
from resolve_2 import get_svg_dict2, str_combine_2
from post_data import post_data, check_exit, get_saved_reviews, update_saved_reviews
import hashlib


def shopReviews(html, shop_url):
    """ 提取店铺评论数据

    :param shop_url:
    :param html: 原网页
    :returns shop_id: 店铺id
    :returns css_dict: css网页中个字段的名称及其坐标


    """
    exit_num = 0
    re_shop_id = re.compile('http://www.dianping.com/shop/(.*?)/review_all')
    re_num = re.compile('[0-9]')
    re_level = re.compile('https://p.*?/squarel(.*?).png')
    shop_id = re.findall(re_shop_id, shop_url)[0]
    m = hashlib.md5()
    doc = pq(html)
    pinglunli = doc("div.reviews-items>ul>li").items()
    shop_pinglun = dict()
    for li in pinglunli:
        pinglun_html = li("div.main-review>div.review-words Hide").html()
        if not pinglun_html:
            pinglun_html = li("div.main-review>div.review-words").html()
        pinglun_text = pinglun_html.replace('<svgmtsi class="', ',').replace('"/>', ',').replace('\n', '').replace(
            ' ', '')
        pinglun_text = re.sub('<imgclass=.*?alt="', '', pinglun_text)
        pinglun_text = re.sub('<divclass=.*?</a></div>', '', pinglun_text)
        supports = li("span.actions>em.col-exp:nth-child(2)").text().replace('(', '').replace(')', '')
        replies = li("span.actions>em.col-exp:nth-child(3)").text().replace('(', '').replace(')', '')
        shop_pinglun['shop_id'] = shop_id
        user_id = li("a.dper-photo-aside").attr('href')
        shop_pinglun['user_id'] = '0'
        if user_id:
            shop_pinglun['user_id'] = ''.join(re.findall(re_num, user_id))

        shop_pinglun['review_time'] = li('span.time').text() + ':00'

        shop_pinglun['name'] = li('div.main-review>div.dper-info>a').text()
        level = li('div.dper-info>img').attr('src')
        if level:
            shop_pinglun['level'] = re.findall(re_level, level)[0].replace('v','')

        if li('div.dper-info>span').attr('class') == 'vip':
            shop_pinglun['vip'] = 1

        star = li("div.main-review>div.review-rank>span").attr('class')
        if star != 'score':
            star_user = re.findall(re_num, star)
            shop_pinglun['star'] = ''.join(star_user)
        shop_pinglun['review'] = pinglun_process(pinglun_text, doc).strip()
        m.update(shop_pinglun['review'].encode('utf-8'))
        shop_pinglun['review_hash'] = m.hexdigest()
        photos = li('div.main-review>div.review-pictures>ul>li').items()
        shop_pinglun['photos'] = num_photos(photos)
        shop_pinglun['photo_urls'] = get_photo_urls(li('div.main-review>div.review-pictures>ul>li').items())
        if supports:
            shop_pinglun['supports'] = supports

        if replies:
            shop_pinglun['replies'] = replies

        # print(shop_pinglun['review'])
        error_num = 0
        # 查重机制
        requests_error_check_num, exit_num = process_time_and_post(shop_pinglun, error_num, exit_num)
        if requests_error_check_num == 1:
            continue
    saved_reviews, re_id = get_saved_reviews('shopreviews', shop_id)
    update_saved_reviews(saved_reviews, re_id)

    return exit_num


def num_photos(photos):
    """ 提取店铺评论数据

    :param photos: 图片url
    :returns num: 图片数


    """
    num = 0
    if photos:
        for item in photos:
            num += 1
    return num


def get_photo_urls(photos):
    urls = '0'
    urls_list = list()
    if photos:
        for item in photos:
            image = item('a>img').attr('data-lazyload')
            urls_list.append(image)
        urls = ','.join(urls_list)
    return urls


def pinglun_process(pinglun_text, doc):
    """ 评论处理函数

    :param pinglun_text: 处理过的有关评论信息
    :param doc: pyquery: 处理过的源代码
    :returns str_pinglun: 用户评论字符串


    """

    head = doc('head')
    pattern = re.compile(r'<link\srel="stylesheet"\stype="text/css"\shref="(.*?)"/>', re.S)
    css_link = re.findall(pattern, head.html())
    css_link = "http:" + css_link[1]
    # 获得css链接
    css_content = requests.get(css_link).text
    re_svg_link = re.compile(r"svgmtsi.*?//([^\s]*);", re.S)
    svg_link = re.findall(re_svg_link, css_content)
    svg_link = "http://" + svg_link[0]
    svg_link = svg_link.replace(')', '')
    # 获得svg链接

    re_css_dict = r".(.*?){background:-(.*?)px -(.*?)px;}"
    css_dict_num = re.findall(re_css_dict, css_content, re.S)
    css_dict = {}
    for data in css_dict_num:
        if '}' in data[0]:
            css_dict[data[0][data[0].rfind('.') + 1:]] = (data[1], data[2])
        else:
            css_dict[data[0]] = (data[1], data[2])

    svg_dict = get_svg_dict1(svg_link)
    if not svg_dict:
        middle_list, svg_dict = get_svg_dict2(svg_link)
        str_pinglun = str_combine_2(middle_list, svg_dict, css_dict, pinglun_text)
    else:
        str_pinglun = str_combine_1(svg_dict, css_dict, pinglun_text)
    return str_pinglun.replace(',', '#$%')


def process_time_and_post(shop_pinglun, error_num, exit_num):
    """ 时间处理与保存到数据库的函数

    :param pinglun_text: 处理过的有关评论信息
    :param error_num: 最大保存错误次数
    :param exit_num: 数据库中已存数据量，若连续出现，最大值为15，若否，清零
    :returns num, exit_num: 检验是否保存成功的参数和数据库中连续已存评论量


    """

    error_num += 1
    try:
        re_review_time = re.compile('(.*?)更新于(.*)')
        if '更' in shop_pinglun['review_time']:
            shop_pinglun['review_time'] = re.findall(re_review_time, shop_pinglun['review_time'])[0][1]
            exit_num, r_check = check_exit(shop_pinglun, exit_num)
            if exit_num == 0:
                post_data('shopreviews', shop_pinglun)

        else:
            exit_num, r_check = check_exit('shopreviews', shop_pinglun, exit_num)
            if exit_num == 0:
                post_data('shopreviews', shop_pinglun)

    except:
        if error_num < 3:
            process_time_and_post(shop_pinglun, error_num, exit_num)
        else:
            return 1, exit_num

    return 0, exit_num


