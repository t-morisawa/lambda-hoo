import re
import random
import requests


def limit(text, limit=100):
    if len(text) > limit:
        return text[0:limit-1] + '...'
    return text

def remove_newline(text):
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\r', '', text)
    return text

class NekoTalker():
    def __init__(self, neko=None):
        self.neko = neko

    def __parse(self, matchobj, is_before=False):
        match_word = matchobj.group(0)
        if is_before is False:
            return self.neko.get_sound() + matchobj.group(0)
        else:
            return matchobj.group(0) + self.neko.get_sound()

    def __parse_before(self, matchobj):
        return self.__parse(matchobj, True)

    def __parse_after(self, matchobj):
        return self.__parse(matchobj, False)

    def parse(self, text):
        text = re.sub(r'？+', self.__parse_after, text)
        text = re.sub(r'\?+', self.__parse_after, text)
        text = re.sub(r'。+', self.__parse_after, text)
        text = re.sub(r'｡+', self.__parse_after, text)
        text = limit(text)
        text = remove_newline(text)
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
        self.name = "クロ校長"

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


class LambdaFoo():
    def __init__(self):
        self.name = "λahoo! 知恵袋"

    def get_icon(self):
        return ':lambda:'

    def talk(self, text):
        return text
