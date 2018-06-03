#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python -*-

import os
import sys

import yaml


class ConfigManager():
    def __init__(self):
        with open(os.path.dirname(os.path.realpath(__file__)) + '/../config/config.yml', 'r') as stream:
            try:
                self.config = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def get_config(self, type):
        if not self.config:
            sys.stderr.write('Unable to read config')
            sys.exit(1)
        else:
            return self.config[type]
