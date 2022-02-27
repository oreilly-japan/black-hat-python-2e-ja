# -*- coding: utf-8 -*-
from burp import IBurpExtender
from burp import IContextMenuFactory

from java.util import ArrayList
from javax.swing import JMenuItem

from datetime import datetime
from HTMLParser import HTMLParser

import re


class TagStripper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.page_text = []

    def handle_data(self, data):
        self.page_text.append(data)

    def handle_comment(self, data):
        self.page_text.append(data)

    def strip(self, html):
        self.feed(html)
        return " ".join(self.page_text)


class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None
        self.hosts = set()

        # よく知られたものから始める
        self.wordlist = set(['password'])

        # 作成した拡張機能をセットする
        callbacks.setExtensionName('BHP Wordlist')
        callbacks.registerContextMenuFactory(self)
        return

    def createMenuItems(self, context_menu):
        self.context = context_menu
        menu_list = ArrayList()
        menu_list.add(JMenuItem(
            "Create Wordlist", actionPerformed=self.wordlist_menu))
        return menu_list

    def wordlist_menu(self, event):
        # ユーザーがクリックした箇所の詳細を取得する
        http_traffic = self.context.getSelectedMessages()
        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            host = http_service.getHost()
            self.hosts.add(host)

            http_response = traffic.getResponse()
            if http_response:
                self.get_words(http_response)
        self.display_wordlist()
        return
    
    def get_words(self, http_response):
        headers, body = http_response.tostring().split('\r\n\r\n', 1)

        # テキストでない部分は飛ばす
        if headers.lower().find("content-type: text") == -1:
            return
        tag_stripper = TagStripper()
        page_text = tag_stripper.strip(body)
        words = re.findall(r'[a-zA-Z]\w{2,}', page_text)

        for word in words:
            # 長い文字列を除去する
            if len(word) <= 12:
                self.wordlist.add(word.lower())
        return

    def mangle(self, word):
        year = datetime.now().year
        suffixes = ['', '1', '!', year]
        mangled = list()
        for password in (word, word.capitalize()):
            for suffix in suffixes:
                mangled.append("%s%s" % (password, suffix))
        return mangled
    
    def display_wordlist(self):
        print("#!comment: BHP Wordlist for site(s) %s" % ", ".join(self.hosts))
        for word in sorted(self.wordlist):
            for password in self.mangle(word):
                print(password)
        return
