# coding: UTF-8
import json
import requests
from question import fetch_question
from changer import NekoTalker, Toro, Kuro, LambdaFoo

with open('slack-config.json', 'r') as f:
    config = json.load(f)

URL_SLACK = config['webhook-url']

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

    # toro (question)
    toro = Toro()
    toro_talk = toro.talk(qa.title)
    post_slack(toro.name, toro.get_icon(), toro_talk + '\n\n' + qa.url)

    # kuro (answer)
    kuro = Kuro()
    kuro_talk = Kuro().talk(qa.ba)
    post_slack(kuro.name, kuro.get_icon(), kuro_talk)

    # lambda
    lambda_foo = LambdaFoo()
    lambda_talk = lambda_foo.talk(qa.title)
    # post_slack(lambda_foo.name, lambda_foo.get_icon(), lambda_talk + '\n\n' + qa.url)

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
