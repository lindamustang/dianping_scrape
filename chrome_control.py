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
from chrome import selemium_chrome


if __name__ == '__main__':
    n = 1
    while n:
        n, browser = selemium_chrome()
        browser.quit()



