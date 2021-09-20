import re
import requests
from pyquery import PyQuery as pq
from fontTools.ttLib import TTFont


character = ['', '', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']


def get_shopMains_num(response):
    """ 总结构函数，用于数字代号和数字间的替换和构建

    :param response: 网页源代码
    :returns num_list: 店铺评论数列表


    """
    html = pq(response)
    css_url = html('head > link:nth-child(23)').attr('href')
    css_url = 'http:' + css_url
    row_num_list = filter_num(response)
    ttf_list, name = get_ttf_list(css_url)
    uni_dict = dict(zip(ttf_list, character))
    num_list = list()
    for row_num in row_num_list:
        if row_num != 0:
            num_for_one = []
            for item1 in row_num:
                if item1 in uni_dict.keys():
                    num = uni_dict[item1]
                    num_for_one.append(num)
                else:
                    num_for_one.append(item1)
            one_num_str = ''.join(num_for_one)
            num_list.append(one_num_str)
        else:
            num_list.append(row_num)

    return num_list


def filter_num(text):
    """ 用于将相关代码清洗，返回相关数字和数字代号列表

    :param text: 网页源代码
    :returns return_list: 返回清洗结果，


    """
    text = text.replace('\n', '').replace('\t', '').replace(' ', '')
    re_filter_1 = r'<divclass="comment">(.*?)<divclass="tag-addr">'
    filter_1 = re.findall(re_filter_1, text, re.S)
    return_list = list()
    for item in filter_1:
        if '我要' in item:
            return_list.append(0)
        else:
            re_filter_2 = r'<b>(.*?)</b>条'
            filter_2 = re.findall(re_filter_2, item, re.S)[0]
            result = re.sub('<svgmtsiclass="shopNum">', ',', filter_2)
            result = re.sub('</svgmtsi>', ',', result)
            result_list_1 = [x for x in result.split(',') if x != '']

            result_list_2 = list()
            for i in result_list_1:
                i = i.replace('&#x', 'uni').replace(';', '')
                result_list_2.append(i)
            return_list.append(result_list_2)
    return return_list


def get_ttf_list(css_url):
    """ 返回0-9数字的代号

    :param css_url: woff文件地址
    :returns uni_list[0:12]: 0-9的数字代号
    :returns name: 下载完毕的woff文件名


    """

    css_text = requests.get(url=css_url).text
    re_url = r'shopNum.*?,url(.*?);}'
    woff_url = re.search(re_url, css_text, re.S).group(1).replace('("', '').replace('")', '')
    name = woff_url[woff_url.rfind('/')+1:-5]
    woff_url = 'http:' + woff_url
    with open(name + '.woff', 'wb') as f:
        f.write(requests.get(url=woff_url).content)
        f.close()
    font = TTFont(name + '.woff')
    uni_list = font['cmap'].tables[0].ttFont.getGlyphOrder()
    return uni_list[0:12], name






