from pyquery import PyQuery as pq
from settings import SERVICE_ENDPOINT, SERVICE_SECRET


def get_photos(html):
    doc = pq(html)
    shop_taps = doc('div#shoptabs-wrapper')
    photos = shop_taps('div.shop-tab-photos.clearfix.J-panel>div.container.clearfix')
    if photos:
        all_img = photos('a').items()
        urls_list = list()
        for img in all_img:
            url = img('img').attr('src')
            urls_list.append(url)
        urls = ','.join(urls_list)






