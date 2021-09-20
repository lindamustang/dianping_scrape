import re
import json
import time
import mitmproxy
import requests
from mitmproxy import ctx
from shopReviews import shopReviews
from shopDetails import shopDetails
from scrape_new_reviews import distribute_last_review
from add_referer import review_pages_referer, shop_detail_referer, shop_index_referer


class Add_uaer_agent_1:
    def __init__(self):
        self.num = 0
        # self.user_agent = get_user_agent(self.num)

    def request(self, flow: mitmproxy.http.HTTPFlow):
        """ 在headers添加user_agent,仅在每次打开mitmproxy时产生变化

        :param flow: mitmproxy.http.HTTPFlow: 数据流

        """

        if 'http' in flow.request.url:
            if 'User-Agent' in flow.request.headers:
                flow.request.headers["User-Agent"] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'


class Add_referer:
    def __init__(self):
        self.num = 0

    def request(self, flow: mitmproxy.http.HTTPFlow):
        """ 在headers添加Referer

        :param flow: mitmproxy.http.HTTPFlow: 数据流

        """

        re_shop_urls = re.compile('^http://www.dianping.com/shop/(.*)')
        re_shop_id = re.compile('(.*?)/review_all')
        re_thirdtoken = re.compile('thirdtoken=.*?;\s')
        text = re_shop_urls.findall(flow.request.url)
        if text:
            text = text[0]
            # shop_id和shop_id/review_all的结合，需要分辨
            if 'review_all' in text:
                shop_id = re.findall(re_shop_id, text)[0]
                refer_url = review_pages_referer(text, shop_id)
                flow.request.headers["Referer"] = refer_url
            else:
                # 此时text是shop_id
                refer_url = shop_detail_referer(text)
                flow.request.headers["Referer"] = refer_url
            print('Referer:' + flow.request.headers["Referer"])
            flow.request.headers['Cookie'] = re.sub(re_thirdtoken, '', flow.request.headers['Cookie'])

        elif '/shanghai/ch10' in flow.request.url:
            refer_url = shop_index_referer(flow.request.url)
            flow.request.headers["Referer"] = refer_url
            print('Referer:' + flow.request.headers["Referer"])

        else:
            pass


class del_Proxy_Connection:
    def __init__(self):
        self.num = 0

    def request(self, flow: mitmproxy.http.HTTPFlow):
        if 'www.dianping.com/' in flow.request.url:
            if '/shanghai/' or '/shop/' in flow.request.url:
                del flow.request.headers["Proxy-Connection"]
                flow.request.headers["Connection"] = "keep-alive"
                print(flow.request.headers["Connection"])


class select_shop_by_id:
    def __init__(self):
        self.num = 0
        self.shop_id = 0
        self.start_page = 0

    def response(self, flow: mitmproxy.http.HTTPFlow):
        # if flow.request.url == 'http://www.dianping.com/':
        #     self.shop_id, self.start_page, self.num = distribute_id(self.num)
        #     details_url = 'shop/' + self.shop_id
        #     change_html = re.sub(r'<head>',
        #                          '<head>\n<script type="text/javascript" defer="defer">\nsetTimeout(() => {\nconsole.log("the code is working!!!");\nwindow.location = "' + details_url + '"},10000);\n</script>',
        #                          flow.response.text)
        #     flow.response.set_text(change_html)
        # if 'www.dianping.com/shop/' in flow.request.url and '/review_all' not in flow.request.url:
        #     review_url = self.shop_id + '/review_all'
        #     if self.start_page > 0:
        #         review_url = self.shop_id + '/review_all/p' + str(self.start_page)
        #     change_html = re.sub(r'<head>',
        #                          '<head>\n<script type="text/javascript" defer="defer">\nsetTimeout(() => {\nconsole.log("the code is working!!!");\nwindow.location.href = "' + review_url + '"},10000);\n</script>',
        #                          flow.response.text)
        #     flow.response.set_text(change_html)

        if 'graph.qq.com' in flow.request.url:
            change_html = re.sub(r'<head>',
                                 '<head>\n<script type="text/javascript">\ndelete '
                                 'navigator.__proto__.webdriver;delete navigator.webdriver;delete '
                                 'navigator.webdriver;delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;delete '
                                 'window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;delete '
                                 'window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;</script>',
                                 flow.response.text)
            flow.response.set_text(change_html)

        elif flow.request.url == 'http://www.dianping.com/':
            # self.shop_id, self.start_page, self.num = distribute_id(self.num)
            # review_url = 'shop/' + self.shop_id + '/review_all'
            # if self.start_page > 0:
            #     review_url = 'shop/' + self.shop_id + '/review_all/p' + str(self.start_page)
            review_url = distribute_last_review()
            change_html = re.sub(r'<head>',
                                 '<head>\n<script type="text/javascript">\ndelete '
                                 'navigator.__proto__.webdriver;delete navigator.webdriver;delete '
                                 'navigator.webdriver;delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;delete '
                                 'window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;delete '
                                 'window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;</script>\n<script type="text/javascript" '
                                 'defer="defer">\nsetTimeout(() => {\nconsole.log("the code is '
                                 'working!!!");\nwindow.location.href = "' + review_url + '"},10000);\n</script>',
                                 flow.response.text)
            flow.response.set_text(change_html)


class Save_1:
    """ """
    def __init__(self):
        self.num = 0

    def response(self, flow: mitmproxy.http.HTTPFlow):
        """ 拦截索引页面和review第一页，生成shopMains,shopDetails和一页shoprReview

        :param flow: mitmproxy.http.HTTPFlow: 数据流

        """
        re_for_details = re.compile('http://www.dianping.com/shop/(.*?)/review_all$')
        # if 'http://www.dianping.com/shanghai/ch10/' in flow.request.url:
        #     if flow.response.text:
        #         shopMains(flow.response.content.decode('utf-8'))
        #         self.num += 1
        #         ctx.log.info("We've saved %d flows" % self.num)

        if re_for_details.findall(flow.request.url):
            shopDetails(flow.response.text, flow.request.url)


class Save_2:
    """ """
    def __init__(self):
        self.num = 0

    def response(self, flow: mitmproxy.http.HTTPFlow):
        """ 仅仅拦截用户评论页面,

        :param flow: mitmproxy.http.HTTPFlow: 数据流

        """
        if '/review_all' in flow.request.url:
            if flow.response.text:
                check_num = shopReviews(flow.response.text, flow.request.url)
                if check_num == 15:
                    # 调回点评首页，重选shop_id
                    change_html = re.sub(r'<head>',
                                                 '<head>\n<script type="text/javascript">\ndelete '
                                                 'navigator.__proto__.webdriver;delete navigator.webdriver;delete '
                                                 'navigator.webdriver;delete '
                                                 'window.cdc_adoQpoasnfa76pfcZLmcfl_Array;delete '
                                                 'window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;delete '
                                                 'window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;</script>\n<script '
                                                 'type="text/javascript" defer="defer">\nwindow.location.pathname = '
                                                 '"";\n</script>',
                                                 flow.response.text)
                    flow.response.set_text(change_html)

                    print('评论重复点到了')


class Add_js:
    def __init__(self):
        self.num = 0

    def response(self, flow: mitmproxy.http.HTTPFlow):
        """ 为用户评论页面,添加js代码

        :param flow: mitmproxy.http.HTTPFlow: 数据流

        """

        if '/review_all' in flow.request.url:
            if flow.response.text:
                sub_html = '<head>\n<script type="text/javascript">\ndelete navigator.__proto__.webdriver;delete ' \
                               'navigator.webdriver;delete navigator.webdriver;delete ' \
                               'window.cdc_adoQpoasnfa76pfcZLmcfl_Array;delete ' \
                               'window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;delete ' \
                               'window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;</script>\n<script type="text/javascript" ' \
                               'defer="defer">\nsetTimeout(() => {\nconsole.log("the code is working!!!")\nlet next = ' \
                               'document.querySelector("a.NextPage");\nlet check_review = document.querySelector(' \
                               '"div.back-to-home")\nif(next != null){\nnext.click();\n}else if(next == null && ' \
                               'check_review != null){window.location.reload();}else{\nwindow.location.pathname = ' \
                               '"";}\n},10000);\n</script> '
                change_html = re.sub(r'<head>',
                                     sub_html,
                                     flow.response.text)
                flow.response.set_text(change_html)


class check_page:
    def __init__(self):
        self.end_pages = ''
        self.num = 0

    def response(self, flow: mitmproxy.http.HTTPFlow):
        """ 为用户评论页面,添加js代码

        :param flow: mitmproxy.http.HTTPFlow: 数据流

        """

        if '/review_all' in flow.request.url:
            self.end_pages = flow.request.url
            self.num = 0

        if 'verify.meituan.com' in flow.request.url and self.num == 0:
            with open('end_pages.txt', 'a', encoding='utf-8') as f:
                f.write(self.end_pages)
                f.write('\n')
            self.num += 1



addons = [
                # Add_uaer_agent_1(),
                Add_referer(),
                Add_js(),
                del_Proxy_Connection(),
                select_shop_by_id(),
                check_page(),
                Save_1(),
                Save_2(),
            ]