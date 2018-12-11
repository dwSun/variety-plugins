#!/usr/bin/env python
# -*- coding: utf-8 -*-
from variety.plugins.IQuoteSource import IQuoteSource
from gettext import gettext as _
import logging

logger = logging.getLogger("variety")


class LocalFilesSource(IQuoteSource):
    def __init__(self):
        super(IQuoteSource, self).__init__()

    @classmethod
    def get_info(cls):
        return {
            "name": "joke",
            "description": _("jokes from laifudao"),
            "author": "dwSun",
            "version": "0.2"
        }

    def supports_search(self):
        return False

    def activate(self):
        if self.active:
            return

        super(LocalFilesSource, self).activate()

        self.quotes = []
        import requests
        url = "http://api.laifudao.com/open/xiaohua.json"

        response = requests.request("GET", url)
        self.quotes = [{'quote': j['title'] + '\n' + self.rm_br(j['content']),
                        'author': j['poster'],
                        'link': j['url'],
                        'sourceName': j['title']} for j in response.json()]

    def deactivate(self):
        self.quotes = []

    def rm_br(self, content):
        while '<br/>' in content:
            content = content.replace('<br/>', '\n')
        while '\n\n' in content:
            content = content.replace('\n\n', '\n')
        return content

    def get_random(self):
        return self.quotes

    def get_for_author(self, author):
        return self.quotes

    def get_for_keyword(self, keyword):
        return self.quotes
