import re


def distribute_last_review():
    with open('end_pages.txt', 'r') as f:
        location = f.readline().strip()
        last = f.readlines()
    re_url = 'http://www.dianping.com/(.*)'
    locate = re.findall(re_url, location)[0]
    with open('end_pages.txt', 'w', encoding='utf-8') as fw:
        for i in last:
            fw.write(i)
    return locate







