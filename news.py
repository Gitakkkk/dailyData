from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
import os
import requests
import smtplib
import dotenv
import mariadb
import datetime

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

conn = mariadb.connect(
    user=os.environ['DBUser'],
    password=os.environ['DBPW'],
    host=os.environ['DBHost'],
    port=int(os.environ['DBPort']),
    database=os.environ['DBName']
)
cur = conn.cursor() 

def insertData(title, link):
    print(title, link)
    try:
        cur.execute("insert into news (title, link, date) values (?, ?, ?)", (title, link, datetime.datetime.now().strftime('%y-%m-%d %H:%M')))
    except mariadb.Error:
        print(f"db insert error: {mariadb.Error}")

titles = []
links = []

# 한경비즈니스
res = requests.get('https://magazine.hankyung.com/tag/%EC%9E%AC%ED%85%8C%ED%81%AC')
soup = BeautifulSoup(res.content, 'lxml')
articles = soup.find_all('h3', attrs={'class':'news-tit'})
for i in range(3):
    title = articles[i].text
    link = articles[i].a['href']
    insertData(title, link)
    titles.append(title)
    links.append(link)

# 매경이코노미
res = requests.get('https://www.mk.co.kr/economy/list/money/')
soup = BeautifulSoup(res.content, 'lxml')
articles = soup.find_all('dt', attrs={'class':'tit'})
for i in range(3):
    title = articles[i].text.split('\n')[1]
    link = articles[i].a['href']
    insertData(title, link)
    titles.append(title)
    links.append(link)

# 한경닷컴 
res = requests.get('https://www.hankyung.com/economy')
soup = BeautifulSoup(res.content, 'lxml')
articles = soup.find_all('h2', attrs={'class':'news-tit'})
for i in range(3):
    title = articles[i].text
    link = articles[i].a['href']
    insertData(title, link)
    titles.append(title)
    links.append(link)

# 매일경제
res = requests.get('https://www.mk.co.kr/news/economy/')
soup = BeautifulSoup(res.content, 'lxml')
articles = soup.find_all('a', attrs={'class':'news_item'})
for i in range(10, 13):
    title = articles[i].h3.text
    link = articles[i]['href']
    insertData(title, link)
    titles.append(title)
    links.append(link)

conn.commit()
conn.close()

msg = MIMEMultipart('alternative')
내용 = f"""
<h2>뉴스 리스트 (06시 기준)</h2>
<h4>{titles[0]} ({links[0]})</h4>
<h4>{titles[1]} ({links[1]})</h4>
<h4>{titles[2]} ({links[2]})</h4>
<h4>{titles[3]} ({links[3]})</h4>
<h4>{titles[4]} ({links[4]})</h4>
<h4>{titles[5]} ({links[5]})</h4>
<h4>{titles[6]} ({links[6]})</h4>
<h4>{titles[7]} ({links[7]})</h4>
<h4>{titles[8]} ({links[8]})</h4>
<h4>{titles[9]} ({links[9]})</h4>
<h4>{titles[10]} ({links[10]})</h4>
<h4>{titles[11]} ({links[11]})</h4>
"""
content = MIMEText(내용, "html")
msg.attach(content)
 
msg['Subject'] ="뉴스 리스트 (06시 기준)"
msg['From'] = 'stom1028@naver.com'
msg['To'] = 'tak.read2@gmail.com'
print(msg.as_string())

s = smtplib.SMTP( 'smtp.naver.com' , 587 ) 
s.starttls() #TLS 보안 처리
s.login( os.environ['NAVERID'] , os.environ['NAVERPW'] ) #네이버로그인
s.sendmail( 'stom1028@naver.com', 'tak.read2@gmail.com', msg.as_string() )
s.close()