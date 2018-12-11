#!/usr/bin/env python
# -*- coding: utf-8 -*-
from variety.plugins.IQuoteSource import IQuoteSource
from gettext import gettext as _
import logging

logger = logging.getLogger("variety")


idioms = "/home/david/Code/chinese-xinhua/data/idiom.json"
xiehou = "/home/david/Code/chinese-xinhua/data/xiehouyu.json"
words = "/home/david/Code/chinese-xinhua/data/word.json"


class XinHuaDict(IQuoteSource):
    def __init__(self):
        super(IQuoteSource, self).__init__()

    @classmethod
    def get_info(cls):
        return {
            "name": "XinHuaDict",
            "description": _("XinHuaDict"),
            "author": "dwSun",
            "version": "0.1"
        }

    def supports_search(self):
        return False

    def activate(self):
        if self.active:
            return

        super(XinHuaDict, self).activate()
        import json
        import random

        self.quotes = []

        with open(idioms) as inf:
            j_idisom = json.load(inf)

        self.quotes.extend([{'quote': '成语：{}\n拼音：{}\n释义：{}\n语出：{}\n示例：{}'.format(
            item['word'], item['pinyin'], item['explanation'],
            item['derivation'], item['example'])} for item in j_idisom])

        with open(xiehou) as inf:
            j_xiehou = json.load(inf)

        self.quotes.extend([{'quote': '{}\n{}'.format(
            item['riddle'], item['answer'])} for item in j_xiehou])

        with open(words) as inf:
            j_word = json.load(inf)

        self.quotes.extend([{'quote': '{}\n拼音：{}\n笔画：{}\n偏旁：{}\n释义：{}\n更多：{}\n'.format(
            item['word'] if item['word'] == item['oldword'] else "{}({})".format(
            item['word'], item['oldword']), item['pinyin'], item['strokes'], item['radicals'],
            item['explanation'], item['more'])} for item in j_word])

        for item in self.quotes:
            item['author'] = ''
            
        random.shuffle(self.quotes)

    def deactivate(self):
        self.quotes = []

    def get_random(self):
        return self.quotes

    def get_for_author(self, author):
        return self.quotes

    def get_for_keyword(self, keyword):
        return self.quotes
