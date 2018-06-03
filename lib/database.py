#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python -*-

import MySQLdb


class Database():
    def __init__(self, config_manager):
        config = config_manager.get_config('database')
        self.db = MySQLdb.connect(config['host'], config['user'], config['password'], config['name'])

    def get_task(self):
        query = self.db.cursor()
        query.execute("SELECT name,value FROM config WHERE name = 'updateBankStatement'")
        ret = query.fetchall()
        return ret[0][1]

    def update_task(self):
        update = self.db.cursor()
        update.execute("UPDATE config SET value = 0  WHERE name = 'updateBankStatement'")
        self.db.commit()
