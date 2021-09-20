import re
import mitmproxy
from create_js_code import js_code
from shopMains import shopMains


class Process_1:
    def __init__(self):
        self.num = 0
        # self.user_agent = get_user_agent(self.num)

    # def request(self, flow: mitmproxy.http.HTTPFlow):
        """ 在headers添加user_agent,仅在每次打开mitmproxy时产生变化

        :param flow: mitmproxy.http.HTTPFlow: 数据流

        """

        # if 'http' in flow.request.url:
        #     flow.request.headers["User-Agent"] = self.user_agent
        #     self.num += 1

    def response(self, flow: mitmproxy.http.HTTPFlow):
        """ 中介获取大众点评店铺索引页面，使用shopMains处理索引页面的信息

        :param flow: mitmproxy.http.HTTPFlow: 数据流

        """

        if '/shanghai/ch10/' in flow.request.url and 'baidu' not in flow.request.url:
            try:
                shopMains(flow.response.text)
                self.num += 1
            except:
                pass


class Process_2:
    def __init__(self):
        self.num = 0

    def request(self, flow: mitmproxy.http.HTTPFlow):
        if 'shanghai/ch10/' in flow.request.url:
            del flow.request.headers["Proxy-Connection"]
            flow.request.headers["Connection"] = "keep-alive"
            print(flow.request.headers["Connection"])

    def response(self, flow: mitmproxy.http.HTTPFlow):
        """ 在headers添加user_agent,仅在每次打开mitmproxy时产生变化

        :param flow: mitmproxy.http.HTTPFlow: 数据流

        """

        if '/shanghai/ch10/g' in flow.request.url:
            change_html = re.sub(r'<head>',
                                 '<head>\n<script type="text/javascript" defer="defer">\nsetTimeout(() => {\nconsole.log("the code is working!!!");\nvar next = document.querySelector("a.next");\nif(next != null){\nnext.click();\n}else{\nwindow.location.pathname = "";}\n},8000);\n</script>',
                                 flow.response.text)
            change_html = re.sub(r'<head>',
                                 '<head>\n<script type="text/javascript" defer="defer">\nsetTimeout(() => {\nconsole.log("the code is working!!!");\nvar not_found = document.querySelector("div.not-found-right");\nif(not_found != null){\nwindow.location.pathname = "";}\n},10000);\n</script>',
                                 change_html)

            flow.response.set_text(change_html)
        elif flow.request.url == "http://www.dianping.com/" or ("www.dianping.com" and "cpt=" in flow.request.url):
            code = js_code()
            change_html = re.sub(r'<head>',
                                 '<head>\n<script type="text/javascript" defer="defer">\n' + code + '\n</script>',
                                 flow.response.text)
            flow.response.set_text(change_html)


addons = [
    Process_1(),
    Process_2()
]
