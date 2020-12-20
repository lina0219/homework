import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.number
songs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

for song in songs:
    rank = song.find('td', {'class': 'number'})
    a_tag = song.select('td.info > a')
    title = song.find('a',{'class':'title ellipsis'})
    artist = song.find('a', {'class': 'artist ellipsis'})
    print(rank.text[0] + rank.text[1].strip(), title.text.strip(), artist.text.strip())
    doc = {
        'rank' : rank.text[0] + rank.text[1].strip(),
        'title' : title.text.strip(),
        'artist' : artist.text.strip()
    }
    db.top50.insert_one(doc)