#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python -*-
import os
import re
import sys
import time

import pyvirtualdisplay
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select, WebDriverWait

from .constants import NATWEST_URL


class Natwest():
    timeout = 10

    def __init__(self, configmananger):
        display = pyvirtualdisplay.Display(visible=0, size=(1280, 1024,))
        display.start()

        self.driver = webdriver.Firefox(self.get_profile())
        self.config = configmananger.get_config('natwest')
        self.main()
        time.sleep(2)
        self.driver.quit()
        display.stop()

    # main functions
    def main(self):
        self.get_page()
        self.enter_customer_number()
        self.login()
        self.download_statement()

    def get_profile(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.dir', os.path.dirname(os.path.realpath(__file__)) + "/../tmp")
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
        return profile

    def get_page(self):
        self.driver.get(NATWEST_URL)

    #        html = self.driver.page_source
    #        print(html)

    def wait_for_iframe_load(self):
        try:
            # Waiting until iframe loads
            element_present = expected_conditions.presence_of_element_located((By.ID, 'aspnetForm'))
            WebDriverWait(self.driver, self.timeout).until(element_present)
        except TimeoutException:
            sys.stderr.write('Timed out waiting for iframe to load')
            sys.exit(1)
        # Additional time for load js with title...
        time.sleep(2)

    def enter_customer_number(self):
        try:
            # Waiting until iframe loads
            element_present = expected_conditions.presence_of_element_located((By.ID, 'ctl00_secframe'))
            WebDriverWait(self.driver, self.timeout).until(element_present)
        except TimeoutException:
            sys.stderr.write('Timed out waiting for page to load')
            sys.exit(1)

        self.driver.switch_to.frame(
            self.driver.find_element_by_id('ctl00_secframe')
        )

        self.wait_for_iframe_load()
        if self.driver.title != 'Log in to Online Banking':
            sys.stderr.write('Wrong page title')
            sys.exit(1)

        form = self.driver.find_element_by_name('aspnetForm')
        customer_number = form.find_element_by_id('ctl00_mainContent_LI5TABA_CustomerNumber_edit')
        customer_number.send_keys(self.config['customer_number'])
        form.submit()
        self.driver.switch_to.default_content()

    def login(self):
        try:
            # Waiting until iframe loads
            element_present = expected_conditions.presence_of_element_located((By.ID, 'ctl00_secframe'))
            WebDriverWait(self.driver, self.timeout).until(element_present)
        except TimeoutException:
            sys.stderr.write('Timed out waiting for page to load')
            sys.exit(1)

        self.driver.switch_to.frame(
            self.driver.find_element_by_id('ctl00_secframe')
        )

        self.wait_for_iframe_load()
        # something wrong with wait for iframe load...
        if self.driver.title.encode('utf8') != 'Log in – PIN and password details':
            sys.stderr.write('Wrong page title')
            sys.exit(1)

        form = self.driver.find_element_by_name('aspnetForm')
        pin = list(self.config['pin'])
        password = list(self.config['password'])
        i = 0
        for char in 'ABCDEF':
            element = form.find_element_by_id('ctl00_mainContent_Tab1_LI6DDAL{0}Label'.format(char))
            psk = re.search('Enter the (\d+)[a-z]{2}', element.text)
            char_num = int(psk.group(1)) - 1
            if i <= 2:
                psk = pin[char_num]
            else:
                psk = password[char_num]

            customer_number = form.find_element_by_id('ctl00_mainContent_Tab1_LI6PPE{0}_edit'.format(char))
            customer_number.send_keys(psk)
            i += 1

        form.submit()

    # TODO: project should be suspended till natwest repair this function...
    def download_statement(self):
        self.wait_for_iframe_load()
        if self.driver.title != 'Account summary':
            sys.stderr.write('Wrong page title')
            sys.exit(1)

        # click statements link
        self.driver.find_element_by_link_text('Statements').click()
        self.driver.find_element_by_link_text('Download or export transactions').click()
        self.wait_for_iframe_load()
        form = self.driver.find_element_by_name('aspnetForm')
        time_period = Select(form.find_element_by_id('ctl00_mainContent_SS6SPDDA'))
        export_type = Select(form.find_element_by_id('ctl00_mainContent_SS6SDDDA'))
        '''
        Available time period:
        - Since last download
        - Last week
        - Last two weeks
        - Last 1 month (4 weeks)
        - Last 2 months
        - Last 3 months
        - Last 4 months
        Available Format Types:
        - Excel, Lotus 123, Text (CSV file)  
        '''
        time_period.select_by_visible_text('Last 2 months')
        export_type.select_by_visible_text('Excel, Lotus 123, Text (CSV file)')
        form.submit()
        # catching errors
        form_error = self.driver.find_element_by_id('ctl00_mainContent_ValidationSummary').text
        if form_error != "":
            sys.stderr(form_error)
            sys.exit(1)
        self.wait_for_iframe_load()
        form = self.driver.find_element_by_name('aspnetForm')
        form.find_element_by_id('ctl00_mainContent_SS7-LWLA_button_button').click()

    def download_statement_alternative(self):
        self.wait_for_iframe_load()
        if self.driver.title != 'Account summary':
            sys.stderr.write('Wrong page title')
            sys.exit(1)

        # click statements link
        self.driver.find_element_by_link_text('Statements').click()
        self.driver.find_element_by_link_text('Search transactions').click()
        form = self.driver.find_element_by_name('aspnetForm')
        time_period = Select(form.find_element_by_id('ctl00_mainContent_VT2SPDDA'))
        transaction_type = Select(form.find_element_by_id('ctl00_mainContent_VT2TTDDA'))
        '''
        Available transaction types:
        - All Transactions
        - ATM Transaction
        - Cash & Dep Machine
        - Charges
        - Cheques
        - Credit Transactions
        - Debit Transactions
        - Direct Debits
        - Dividends
        - Interest
        - International Transactions
        - Payroll
        - Standing Orders
        - Debit Card Payments
        - Telephone Banking
        - OnLine Banking        
        '''
        time_period.select_by_visible_text('Last two weeks')
        transaction_type.select_by_visible_text('All Transactions')
        form.submit()
        self.wait_for_iframe_load()
        form = self.driver.find_element_by_name('aspnetForm')
        form.find_element_by_id('ctl00_mainContent_VT2ITCHF').click()
        select_format = Select(form.find_element_by_id('ctl00_mainContent_VTSDDDA'))
        select_format.select_by_visible_text('Excel, Lotus 123, Text (CSV file)')
        self.wait_for_iframe_load()
        form = self.driver.find_element_by_name('aspnetForm')
        form.find_element_by_id('ctl00_mainContent_SS7-LWLA_button_button').click()
