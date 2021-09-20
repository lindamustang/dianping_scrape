import time
import requests
import random
import selenium
from PIL import Image
from datetime import date, timedelta
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options


def is_pixel_equal(image1, image2, x, y):
    """
    判断两张图片 各个位置的像素是否相同
    :param image1:不带缺口的图片
    :param image2: 带缺口的图片
    :param x: 位置x
    :param y: 位置y
    :return: (x,y)位置的像素是否相同
    """
    # 获取两张图片指定位置的像素点
    pixel1 = image1.load()[x, y]
    pixel2 = image2.load()[x, y]
    # 设置一个阈值 允许有误差
    threshold = 60
    # 彩色图 每个位置的像素点有三个通道
    if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
            pixel1[2] - pixel2[2]) < threshold:
        return True
    else:
        return False


def process_photos(url):
    photo = requests.get(url)
    ful_url = url[:-10] + '0&subsid=3'
    ful_photo = requests.get(ful_url)
    with open('1.jpg', 'wb') as f1:
        f1.write(photo.content)
    with open('2.jpg', 'wb') as f2:
        f2.write(ful_photo.content)
    image_a = Image.open('1.jpg')
    image_b = Image.open('2.jpg')
    new_image_a = image_a.resize((290, 163), Image.BILINEAR)
    new_image_b = image_b.resize((290, 163), Image.BILINEAR)
    for i in range(145, new_image_a.size[0]):  # 从左到右 x方向
        for j in range(new_image_a.size[1]):  # 从上到下 y方向
            if not is_pixel_equal(new_image_a, new_image_b, i, j):
                left = i  # 找到缺口的左侧边界 在x方向上的位置
                return left


def wait_for_check(browser):
    element = WebDriverWait(browser, 40000, poll_frequency = 5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "yoda-slider-wrapper"))
    )
    return element


# if __name__ == '__main__':
def selemium_chrome():
    options = Options()
    proxy = '127.0.0.1:8080'
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--disable-web-security")
    # options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)
    # Chrome/91.0.4472.114 Safari/537.36')
    options.add_argument('-proxy-server=http://' + proxy)
    browser = webdriver.Chrome(options=options)
    browser.get('https://account.dianping.com/thirdconnect?do=l&ft=6&redir=http%3A%2F%2Fwww.dianping.com')
    browser.switch_to.frame('ptlogin_iframe')
    browser.find_element_by_id('switcher_plogin').click()
    name = browser.find_element_by_id('u')
    name.send_keys('你的qq')
    passwd = browser.find_element_by_id('p')
    passwd.send_keys('qq密码')
    time.sleep(0.2)
    browser.find_element_by_id('login_button').click()
    time.sleep(2)
    try:
        browser.switch_to.frame('tcaptcha_iframe')
        photo_url = browser.find_element_by_id('slideBg').get_attribute('src')
        distance = process_photos(photo_url) - random.uniform(16.5, 17.5) - 22.5
        silder = browser.find_element_by_id('tcaptcha_drag_thumb')
        time.sleep(0.3)
        ActionChains(browser).click_and_hold(silder).perform()
        ActionChains(browser).move_by_offset(xoffset=distance, yoffset=0).perform()
        ActionChains(browser).release().perform()

    except:
        pass

    try:
        ele = wait_for_check(browser)
        return ele, browser
    except:
        ele = wait_for_check(browser)
        return ele, browser
