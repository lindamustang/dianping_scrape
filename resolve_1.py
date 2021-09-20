import re
import requests


def get_phone_svg(svg_link):
    """ 用于商铺电话处理的svg函数

    :param svg_link: 在大众点评css样式页面中截取的svg链接（用于电话）
    :return svg_dict: 构造后的svg字典（数字）


    """
    svg_html = requests.get(svg_link)
    svg_dict = {}
    re_svg_list = re.compile(r'<text.*?>(.*?)</text>', re.S)
    svg_dict_re = re.findall(re_svg_list, svg_html.text)[0]
    for i in range(10):
        svg_dict[i] = svg_dict_re[i]
    return svg_dict

    # for data in svg_dict_re:
    #     svg_dict[data[0]] = list(data[1])
    # return svg_dict


def get_svg_dict1(svg_link):
    """ svg字典构造的第一种方法

    :param svg_link: 在大众点评css样式页面中截取的svg链接（用于文本）
    :return svg_dict: 构造后的svg字典（文字）

    """
    svg_html = requests.get(svg_link)
    svg_dict = {}
    re_svg_list = re.compile(r'<text x="0" y="(.*?)">(.*?)</text>', re.S)
    svg_dict_re = re.findall(re_svg_list, svg_html.text)
    for data in svg_dict_re:
        svg_dict[data[0]] = list(data[1])
    return svg_dict


def str_combine_1(svg_dict, css_dict, pinglun_text):
    """ 评论或是其他信息构造函数

    :param svg_dict: 构建的svg字典
    :param css_dict: 构建的css字典
    :param pinglun_text: 大众点评用户评论页面用户评论区域的html代码
    :return str_pinglun: 用户评论字符串


    """
    pinglun_list = [x for x in pinglun_text.split(",") if x != '']
    pinglun_str = list()
    for msg in pinglun_list:
        if msg in css_dict.keys():
            x = int(int(float(css_dict[msg][0])) / 14)
            y = int(float(css_dict[msg][1]))
            for check in svg_dict.keys():
                if y <= int(check):
                    msg = svg_dict[str(check)][x]
                    pinglun_str.append(msg)
                    break

        else:
            pinglun_str.append(msg)
    str_pinglun = ''.join(pinglun_str)
    return str_pinglun


def phone_combine(svg_dict, css_dict, phone_text):
    phone_list = [x for x in phone_text.split(",") if x != '']
    str_list = list()
    for msg in phone_list:
        if msg in css_dict.keys():
            x = int(int(float(css_dict[msg][0])) / 14)
            for check in svg_dict.keys():
                if x == check:
                    str_list.append(svg_dict[x])
                    break

        else:
            str_list.append(msg)
    str_phone = ''.join(str_list)
    return str_phone.replace('\xa0', '&').replace('电话:&', '')

