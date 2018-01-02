#!/usr/bin/env python
# -*- mode: python -*-

from .constants import NATWEST_URL
from selenium import webdriver


class Natwest():
    def __init__(self):
        self.browser = webdriver.Firefox()

    def get_page(self):
        self.browser.get(NATWEST_URL)
        html = self.browser.page_source
        print(html)