# coding: UTF-8
import sys
import random
import urllib.request
import re
import json
import requests
from bs4 import BeautifulSoup

URL_CHIEBUKURO = "https://chiebukuro.yahoo.co.jp/ranking/ranking.php"

def get_soup_obj(url):
    req = urllib.request.Request(url)
    html = urllib.request.urlopen(req)
    return BeautifulSoup(html, "html.parser")

def random_nyaa(matchobj):
    match_word = matchobj.group(0)
    if match_word == '(?)' or match_word == '（？）' or match_word == '(？)' or match_word == '（?）':
        return
    return random.choice(['ニャ', 'ニャ〜', 'ニャ...']) + matchobj.group(0)

def random_nyaa_before(matchobj):
    match_word = matchobj.group(0)
    if match_word == '(?)' or match_word == '（？）' or match_word == '(？)' or match_word == '（?）':
        return
    return matchobj.group(0) + random.choice(['ニャ', 'ニャ〜', 'ニャ...'])

# 文を整形する
def parse_nyaa(text):
    text = re.sub(r'？+', random_nyaa, text)
    text = re.sub(r'\?+', random_nyaa, text)
    text = re.sub(r'。+', random_nyaa, text)
    text = re.sub(r'｡+', random_nyaa, text)
    return text

def run():
    # q&Aを一つ取得
    soup = get_soup_obj(URL_CHIEBUKURO)
    qa_list = soup.find(id="qarnk").find_all('a')
    qa_url = random.choice(qa_list).get("href")
    soup = get_soup_obj(qa_url)
    qa = soup.find(property="og:title").get("content")

    # 質問を加工
    qa = parse_nyaa(qa)

    # 開発用
    print(qa)
    print(qa_url)

    # incoming-webhooks
    slack_url = 'https://hooks.slack.com/services/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'
    icons = [
        ':toro_1:', ':toro_3:', ':toro_4:', ':toro_5:'
    ]
    data = {
        "text": qa + '\n\n' + qa_url,
        "username": "井上トロ",
        "icon_emoji": random.choice(icons)
    }
    headers = {
        "Content-type": "application/json"
    }

    data = json.dumps(data)

    r = requests.post(slack_url, data)

# lambdaのハンドラ
def handler(event, context):
    run()

if __name__ == '__main__':
    run()
