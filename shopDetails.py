import re
import requests
from pyquery import PyQuery as pq
from resolve_1 import get_svg_dict1, get_phone_svg, str_combine_1, phone_combine
from resolve_2 import get_svg_dict2, str_combine_2
from post_data import post_data, check_exit, update_data


def shopDetails(html, shop_url):
    """ 店铺详细信息

    :param html: 原网页
    :param shop_url: 原网页网址

    """

    re_num = re.compile('[0-9]')
    re_shop_id = re.compile('shop/(.*?)/review_all')
    shop_id = re.findall(re_shop_id, shop_url)
    html = pq(html)
    svg_links, css_dict = get_css_svg(html)
    address_html = html('div.address-info').html()
    address_text = address_html.replace('<bb class="', ',').replace('"/>', ',').replace('\n', '').replace(' ', '')
    phone = html('div.phone-info').html()
    shop_details = dict()
    shop_details['shop_name'] = html('div.list-crumb>a:nth-child(4)').text()
    shop_details['shop_id'] = shop_id[0]
    shop_details['type'] = html('div.list-crumb>a:nth-child(2)').text()
    star = html('div.star_icon>span:nth-child(1)').attr('class')
    shop_star = re.findall(re_num, star)
    shop_details['star'] = ''.join(shop_star)
    if html('div.rank-info>span.reviews'):
        reviews = re.findall(re_num, html('div.rank-info>span.reviews').text())

    shop_details['reviews'] = int(''.join(reviews))
    price = re.findall(re_num, html('div.rank-info>span.price').text())
    shop_details['price'] = int(''.join(price))
    shop_details['taste'] = float(html('div.rank-info>span.score>span.item:nth-child(1)').text().replace('口味：', ''))
    shop_details['environment'] = float(
        html('div.rank-info>span.score>span.item:nth-child(2)').text().replace('环境：', ''))
    shop_details['service'] = float(html('div.rank-info>span.score>span.item:nth-child(3)').text().replace('服务：', ''))
    shop_details['district'] = html('div.list-crumb>a:nth-child(3)').text()
    shop_details['address'] = get_message(svg_links, css_dict, address_text, 0)
    if phone:
        phone_text = phone.replace('<cc class="', ',').replace('"/>', ',').replace('\n', '').replace(' ', '')
        shop_details['phone'] = get_message(svg_links, css_dict, phone_text, 1)
    err_num = 0
    check_exit_num, old_data = check_exit('shopdetails', shop_details, 0)
    if check_exit_num == 0:
        process_post_error(err_num, shop_details)
    else:
        process_updata_error(err_num, shop_details, old_data)


def get_css_svg(html):
    """ 处理原网页中的css网页

    :param html: 原网页
    :returns svg_links: svg网页urls
    :returns css_dict: css网页中个字段的名称及其坐标


    """

    head = html('head')
    re_svg_bb = r'{width: 14px;height: 22px;margin-top: -1px;background-image:(.*?);'
    re_svg_cc = r'{width: 14px;height: 16px;margin-top: -7px;background-image:(.*?);'
    pattern = re.compile(r'<link\srel="stylesheet"\stype="text/css"\shref="(.*?)"/>', re.S)
    css_link = re.findall(pattern, head.html())
    css_link = "http:" + css_link[1]
    # 获得css链接
    svg_links = []
    css_content = requests.get(css_link).text
    bb_svg_link = re.findall(re_svg_bb, css_content)[0].replace('url(//', '').strip()
    cc_svg_link = re.findall(re_svg_cc, css_content)[0].replace('url(//', '').strip()
    svg_links.append(bb_svg_link)
    svg_links.append(cc_svg_link)
    re_css_dict = r".(.*?){background:-(.*?)px -(.*?)px;}"
    css_dict_num = re.findall(re_css_dict, css_content, re.S)
    css_dict = {}
    for data in css_dict_num:
        css_dict[data[0]] = (data[1], data[2])
    return svg_links, css_dict


def get_message(svg_links, css_dict, content, num):
    """ 处理店铺电话和地址信息

    :param svg_links: svg网页urls
    :param css_dict: css网页中个字段的名称及其坐标
    :param content: 商铺电话或地址的相关html代码
    :param num: 电话或是店铺地址svg_url在css页面的顺序（后面需要完善正则）
    :returns str_message: 返回的电话或是店铺地址字符串


    """

    svg_link = "http://" + svg_links[num]
    svg_link = svg_link.replace(')', '')
    if num == 0:
        # 此处数字修改成地址次序
        svg_dict = get_svg_dict1(svg_link)
        if not svg_dict:
            middle_list, svg_dict = get_svg_dict2(svg_link)
            str_message = str_combine_2(middle_list, svg_dict, css_dict, content)
            str_message = str_message.replace('\xa0', '').replace('地址:', '')
        else:
            str_message = str_combine_1(svg_dict, css_dict, content).replace('\xa0', '').replace('地址:', '')
    else:
        svg_dict = get_phone_svg(svg_link)
        str_message = phone_combine(svg_dict, css_dict, content)
    return str_message


def process_post_error(err_num, shop_details):
    err_num = err_num + 1
    try:
        post_data('shopdetails', shop_details)

    except requests.exceptions.BaseHTTPError:
        if err_num < 3:
            process_post_error(err_num, shop_details)
        else:
            pass


def process_updata_error(err_num, shop_details, old_data):
    err_num = err_num + 1
    try:
        update_data('shopdetails', shop_details)

    except requests.exceptions.BaseHTTPError:
        if err_num < 3:
            process_updata_error(err_num, shop_details, old_data)
        else:
            pass
