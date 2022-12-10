from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import time

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument(r'/Users/nagitak/Library/Application Support/Google/Chrome/Profile 3')

browser = webdriver.Chrome(executable_path='/Users/nagitak/Desktop/dailyNews/chromedriver', chrome_options=options)
browser.get('https://nid.naver.com/nidlogin.login?svctype=262144&url=https%3A%2F%2Fm.naver.com%2Fna%2F')

# soup = BeautifulSoup(browser.page_source, 'lxml') # html parsing

# def no_space(text):
#     text1 = re.sub('&nbsp; | &nbsp;| \n|\t|\r', '', text)
#     text2 = re.sub('\n\n', '', text1)
#     return text2