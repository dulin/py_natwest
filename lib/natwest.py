#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python -*-

from .constants import NATWEST_URL
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os, sys, time, re
import yaml


class ConfigManager():
    def __init__(self):
        with open(os.environ["HOME"] + "/.py_natwest.yml", 'r') as stream:
            try:
                self.config = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def get_config(self):
        if not self.config:
            sys.stderr.write("Unable to read config")
            sys.exit(1)
        else:
            return self.config


class Natwest():
    timeout = 5

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.config = ConfigManager().get_config()

    def get_page(self):
        self.driver.get(NATWEST_URL)

    #        html = self.driver.page_source
    #        print(html)

    def wait_for_iframe_load(self):
        try:
            # Waiting until iframe loads
            element_present = EC.presence_of_element_located((By.NAME, "aspnetForm"))
            WebDriverWait(self.driver, self.timeout).until(element_present)
        except TimeoutException:
            sys.stderr.write("Timed out waiting for iframe to load")
            sys.exit(1)

    def enter_customer_number(self):

        try:
            # Waiting until iframe loads
            element_present = EC.presence_of_element_located((By.ID, "ctl00_secframe"))
            WebDriverWait(self.driver, self.timeout).until(element_present)
        except TimeoutException:
            sys.stderr.write("Timed out waiting for page to load")
            sys.exit(1)

        self.driver.switch_to.frame(
            self.driver.find_element_by_id("ctl00_secframe")
        )

        self.wait_for_iframe_load()
        if self.driver.title != "Log in to Online Banking":
            sys.stderr.write("Wrong page title")
            sys.exit(1)

        form = self.driver.find_element_by_name("aspnetForm")
        customer_number = form.find_element_by_id("ctl00_mainContent_LI5TABA_CustomerNumber_edit")
        customer_number.send_keys(self.config['customer_number'])
        form.submit()
        self.driver.switch_to.default_content()

    def login(self):
        try:
            # Waiting until iframe loads
            element_present = EC.presence_of_element_located((By.ID, "ctl00_secframe"))
            WebDriverWait(self.driver, self.timeout).until(element_present)
        except TimeoutException:
            sys.stderr.write("Timed out waiting for page to load")
            sys.exit(1)

        self.driver.switch_to.frame(
            self.driver.find_element_by_id("ctl00_secframe")
        )

        self.wait_for_iframe_load()
        # something wrong with wait for iframe load...
        time.sleep(2)

        if self.driver.title.encode('utf8') != "Log in – PIN and password details":
            sys.stderr.write("Wrong page title")
            sys.exit(1)

        form = self.driver.find_element_by_name("aspnetForm")
        letters = "ABCDEF"
        pin = list(self.config['pin'])
        password = list(self.config['password'])
        i = 0
        for letter in letters:
            element = form.find_element_by_id("ctl00_mainContent_Tab1_LI6DDAL" + letter + "Label")
            psk = re.search("Enter the (\d+)[a-z]{2}", element.text)
            char_num = int(psk.group(1)) - 1
            if i <= 2:
                psk = pin[char_num]
            else:
                psk = password[char_num]

            customer_number = form.find_element_by_id("ctl00_mainContent_Tab1_LI6PPE" + letter + "_edit")
            customer_number.send_keys(psk)
            i += 1

        form.submit()
