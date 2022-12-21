from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
# from github import Github, Issue
import pyperclip
import re
import time
import dotenv
import os
import datetime
# import mariadb 

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

# python - mariadb connect
# conn = mariadb.connect(
#     user=os.environ['dbUser'],
#     password=os.environ['dbPW'],
#     host=os.environ['dbHost'],
#     port=int(os.environ['dbPort']),
#     database=os.environ['dbName']
# )
# cur = conn.cursor() 

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument(r'/Users/nagitak/Library/Application Support/Google/Chrome/Profile 3')
options.add_experimental_option("detach", True)

# 필요 없는 개행과 공백 제거
def noSpace(text):
    text1 = re.sub('&nbsp; | &nbsp;| \n|\t|\r', '', text)
    reuslt = re.sub('\n\n', '', text1)
    return reuslt

# 채널 필터링
def textMatch(text):
    if re.search(r'구독자수', text):
        splitText = re.split('\n', text)[3]
        chaanel = re.findall('[가-힣+]', splitText)
        result = ''.join(chaanel)
        return result
    else:
        chaanel = re.findall('[가-힣+]', text)
        result = ''.join(chaanel)
        return result
        
# 브라우저 열고 로그인 후 뉴스 진입
browser = webdriver.Chrome(executable_path='/Users/nagitak/Desktop/dailyNews/chromedriver', chrome_options=options)
browser.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
time.sleep(3)
browser.find_element(By.ID, 'id').click()
pyperclip.copy(os.environ['NAVERID'])
browser.find_element(By.ID, 'id').send_keys(Keys.COMMAND, 'v')
time.sleep(1)
browser.find_element(By.ID, 'pw').click()
pyperclip.copy(os.environ['NAVERPW'])
browser.find_element(By.ID, 'pw').send_keys(Keys.COMMAND, 'v')
time.sleep(1)
browser.find_element(By.ID, 'log.login').click()
time.sleep(3)
browser.get('https://news.naver.com')

soup = BeautifulSoup(browser.page_source, 'lxml') # html parsing

# title & url 크롤링해서 DB에 저장
news = soup.find_all('div', attrs={'class': 'main_brick_item _channel_news_card_wrapper'})
for i in range(len(news)):
    channel = textMatch(news[i].find_all('h4', attrs={'class': 'channel'})[0].text)
    title_first =  news[i].find_all('a', attrs={'class': 'cc_text_a _need_nclick _cds_link'})[0].text
    title_second =  news[i].find_all('a', attrs={'class': 'cc_text_a _need_nclick _cds_link'})[1].text
    title_third =  news[i].find_all('a', attrs={'class': 'cc_text_a _need_nclick _cds_link'})[2].text
    link_first =  news[i].find_all('a', attrs={'class': 'cc_text_a _need_nclick _cds_link'})[0]['href']
    link_second =  news[i].find_all('a', attrs={'class': 'cc_text_a _need_nclick _cds_link'})[1]['href']
    link_third =  news[i].find_all('a', attrs={'class': 'cc_text_a _need_nclick _cds_link'})[2]['href']
    date = datetime.datetime.now().strftime('%y-%m-%d %H:%M')
    print(f'{channel}\n{title_first}\n{link_first}\n{date}\n{channel}\n{title_second}\n{link_second}\n{date}\n{channel}\n{title_third}\n{link_third}\n{date}')
    # try: 
    #     cur.execute("insert into news (channel, title, link, date) values (?, ?, ?, ?)", (channel, title_first, link_first, date))
    #     cur.execute("insert into news (channel, title, link, date) values (?, ?, ?, ?)", (channel, title_second, link_second, date))
    #     cur.execute("insert into news (channel, title, link, date) values (?, ?, ?, ?)", (channel, title_third, link_third, date))
    # except mariadb.Error:
    #     print(f"db insert error: {mariadb.Error}")

# conn.commit()
# conn.close()
browser.quit()
    