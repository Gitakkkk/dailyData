from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyperclip
from bs4 import BeautifulSoup
import re
import time
import dotenv
import os

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument(r'/Users/nagitak/Library/Application Support/Google/Chrome/Profile 3')
options.add_experimental_option("detach", True)

browser = webdriver.Chrome(executable_path='/Users/nagitak/Desktop/dailyNews/chromedriver', chrome_options=options)
browser.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
time.sleep(3)
browser.find_element(By.ID, 'id').click()
pyperclip.copy(os.environ['naverID'])
browser.find_element(By.ID, 'id').send_keys(Keys.COMMAND, 'v')
time.sleep(1)
browser.find_element(By.ID, 'pw').click()
pyperclip.copy(os.environ['naverPW'])
browser.find_element(By.ID, 'pw').send_keys(Keys.COMMAND, 'v')
time.sleep(1)
browser.find_element(By.ID, 'log.login').click()
time.sleep(3)
browser.get('https://news.naver.com')



# soup = BeautifulSoup(browser.page_source, 'lxml') # html parsing

# def no_space(text):
#     text1 = re.sub('&nbsp; | &nbsp;| \n|\t|\r', '', text)
#     text2 = re.sub('\n\n', '', text1)
#     return text2