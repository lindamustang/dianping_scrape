import requests
import re


def get_svg_dict2(svg_link):
    """ svg字典构造的第二种方法

    :param svg_link: 在大众点评css样式页面中截取的svg链接（用于文本）
    :return middle_list: 中间数列
    :return svg_dict: 构造后的svg字典（文字）

    """

    svg_html = requests.get(svg_link)
    re_svg_num = re.compile(r'<path id="(.*?)" d="(.*?) (.*?) (.*?)"/>', re.S)
    svg_y = re.findall(re_svg_num, svg_html.text)
    middle_list = []
    middle_list_ = []
    svg_dict = {}
    for data in svg_y:
        middle_list_.append(data[0])
        middle_list_.append(data[2])
        middle_list.append(middle_list_)
        middle_list_ = []
    re_svg_list = re.compile(r'<textPath xlink:href="(.*?)" textLength="(.*?)">(.*?)</textPath>', re.S)
    svg_dict_re = re.findall(re_svg_list, svg_html.text)
    for data in svg_dict_re:
        svg_dict[data[0].replace('#', '')] = list(data[2])
    return middle_list, svg_dict


def str_combine_2(middle_list, svg_dict, css_dict, pinglun_text):
    """ 评论或是其他信息构造函数

    :param middle_list: 中间数列
    :param svg_dict: 构建的svg字典
    :param css_dict: 构建的css字典
    :param pinglun_text: 大众点评用户评论页面用户评论区域的html代码
    :return str_pinglun: 用户评论以及店铺地址字符串


    """

    pinglun_list = [x for x in pinglun_text.split(",") if x != '']
    pinglun_str = []
    for msg in pinglun_list:
        if msg in css_dict.keys():
            x = int(int(float(css_dict[msg][0])) / 14)
            y = int(float(css_dict[msg][1]))
            for mid_y in middle_list:
                if y <= int(mid_y[1]):
                    svg_y = str(mid_y[0])
                    pinglun_str.append(svg_dict[svg_y][x])
                    break
        else:
            pinglun_str.append(msg)
    str_pinglun = ''.join(pinglun_str)
    return str_pinglun

