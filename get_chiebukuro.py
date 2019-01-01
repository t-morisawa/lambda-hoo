# coding: UTF-8
import sys
import random
import urllib.request
import re
import json
import requests
from bs4 import BeautifulSoup

URL_CHIEBUKURO = "https://chiebukuro.yahoo.co.jp/ranking/ranking.php"
URL_SLACK = 'https://hooks.slack.com/services/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'

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

class NekoTalker():
    def __init__(self, neko):
        self.neko = neko

    def __parse(self, matchobj, is_before=False):
        match_word = matchobj.group(0)
        if match_word == '(?)' or match_word == '（？）' or match_word == '(？)' or match_word == '（?）':
            return
        if is_before is False:
            return self.neko.get_sound() + matchobj.group(0)
        else:
            return matchobj.group(0) + self.neko.get_sound()

    def __parse_before(self, matchobj):
        return self.__parse(matchobj, True)

    def __parse_after(self, matchobj):
        return self.__parse(matchobj, False)

    def __limit(self, st):
        if len(st) > 100:
            return st[0:99] + '...'
        return st

    def parse(self, text):
        text = re.sub(r'？+', self.__parse_after, text)
        text = re.sub(r'\?+', self.__parse_after, text)
        text = re.sub(r'。+', self.__parse_after, text)
        text = re.sub(r'｡+', self.__parse_after, text)
        text = re.sub(r'\n', '', text)
        text = re.sub(r'\r', '', text)
        text = self.__limit(text)
        return text

class Toro():
    def __init__(self):
        self.name = "井上トロ"

    def get_icon(self):
        icons = [
            ':toro_1:', ':toro_3:', ':toro_4:', ':toro_5:'
        ]
        return random.choice(icons)

    def get_sound(self):
        sounds = ['ニャ', 'ニャ〜', 'ニャ...']
        return random.choice(sounds)

    def talk(self, text):
        parser = NekoTalker(self)
        return parser.parse(text)

class Kuro():
    def __init__(self):
        self.name = "クロ先生"

    def get_icon(self):
        icons = [
            ':kuro_1:'
        ]
        return random.choice(icons)

    def get_sound(self):
        sounds = ['みャ', 'みャ〜', 'みャ...', 'ンなー']
        return random.choice(sounds)

    def talk(self, text):
        parser = NekoTalker(self)
        return parser.parse(text)


def post_slack(name, icon, text):
    if text == '':
        return
    data = {
        "text": text,
        "username": name,
        "icon_emoji": icon
    }
    headers = {
        "Content-type": "application/json"
    }
    data = json.dumps(data)
    r = requests.post(URL_SLACK, data)


def run():
    qa = fetch_question()
    toro = Toro()
    kuro = Kuro()
    toro_talk = toro.talk(qa.title)
    kuro_talk = Kuro().talk(qa.ba)

    post_slack(toro.name, toro.get_icon(), toro_talk + '\n\n' + qa.url)
    post_slack(kuro.name, kuro.get_icon(), kuro_talk)

    # # 開発用
    # print(qa.title)
    # print(toro_talk)
    # print(kuro_talk)
    # print(qa.url)


# lambdaのハンドラ
def handler(event, context):
    run()

if __name__ == '__main__':
    run()
