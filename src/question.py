# coding: UTF-8
import random
import urllib.request
from bs4 import BeautifulSoup


URL_CHIEBUKURO = "https://chiebukuro.yahoo.co.jp/ranking/ranking.php"

class Question():
    def __init__(self, url, title, ba):
        self.url = url
        self.title = title
        self.ba = ba

def get_soup_obj(url):
    req = urllib.request.Request(url)
    html = urllib.request.urlopen(req)
    return BeautifulSoup(html, "html.parser")

def fetch_question():
    # q&Aを一つ取得
    soup = get_soup_obj(URL_CHIEBUKURO)
    qa_list = soup.find(id="qarnk").find_all('a')
    qa_url = random.choice(qa_list).get("href")
    soup = get_soup_obj(qa_url)
    qa_title = soup.find(property="og:title").get("content")
    # ベストアンサーがまだない質問がヒットすることもある
    try:
        ba = soup.find(id="ba").find(class_="yjDirectSLinkTarget").text
        return Question(qa_url, qa_title, ba)
    except AttributeError:
        return Question(qa_url, qa_title, '')
