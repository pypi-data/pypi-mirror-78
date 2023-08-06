#!/usr/bin/env python3
# -*- encoding=utf-8 -*-



class BaseButton:

    def __init__(self, button_type, name):
        self.data = {'type': button_type, 'name': name}

    def get_data(self):

        return self.data
