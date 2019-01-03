import json
import random
import time
from question import fetch_question
from requests_oauthlib import OAuth1Session
from changer import Toro, limit

with open('twitter-api.json', 'r') as f:
    api = json.load(f)

CK = api['ck']
CS = api['cs']
AT = api['at']
AS = api['as']
ID = api['id']

UPDATE_URL = 'https://api.twitter.com/1.1/statuses/update.json'
GET_URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

# tweet text
def _tweet(text):
    params = {"status": text }
    twitter = OAuth1Session(CK, CS, AT, AS)
    req = twitter.post(UPDATE_URL, params = params)

    if req.status_code == 200:
        return text
    else:
        return req.status_code

def _get_id():
    twitter = OAuth1Session(CK, CS, AT, AS)
    req = twitter.get(GET_URL + '?count=1&screen_name=chiechiebukuro')

    if req.status_code == 200:
        return json.loads(req.text)[0].get('id')
    else:
        return req.status_code

def _reply(post_id, text):
    params = {
        "status": text,
        "in_reply_to_status_id": post_id
    }
    twitter = OAuth1Session(CK, CS, AT, AS)
    req = twitter.post(UPDATE_URL, params = params)

    if req.status_code == 200:
        return text
    else:
        return req.status_code

def run():
    qa = fetch_question()

    # normal
    # _tweet(qa.title + '\n\n' + qa.url)

    # nyaa
    toro = Toro()
    toro_talk = toro.talk(qa.title)
    post = toro_talk + '\n\n' + qa.url
    print(post)
    _tweet(post)

    time.sleep(1)
    post_ba = '[ベストアンサー]' + limit(qa.ba)
    _reply(_get_id(), ID + ' ' + post_ba)

# lambdaのハンドラ
def handler(event, context):
    run()

if __name__ == '__main__':
    run()
