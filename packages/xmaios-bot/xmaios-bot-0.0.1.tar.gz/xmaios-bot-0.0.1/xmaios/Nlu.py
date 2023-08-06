#!/usr/bin/env python3
# -*- coding=utf-8 -*-

"""
语义解析
"""


class Nlu(object):

    def __init__(self, data):

        super(Nlu, self).__init__()
        self.data = data
        self.ask_slot = None
        self.directive = None
        self.afterSearchScore = None

    def set_intent_token(self, intent_token, index=0):
        """
        :param intent_token:
        :param index:
        :return:
        """
        self.data[index]['token'] = intent_token

    def get_intent_token(self, index=0):
        """
        获取当前的意图intent标识
        :return:
        """

        return self.data[index]['token'] if 'token' in self.data[index] else ''

    def get_intent_name(self, index=0):
        """
        获取当前的意图intent名称
        :return:
        """

        return self.data[index]['name'] if 'name' in self.data[index] else ''

    def set_slot(self, field, value, index=0):
        """
        设置槽位信息
        desc 设置slot, 如果不存在,slot
        :param field:   槽位名
        :param value:   槽位值
        :param index:  第几组slot
        :return:
        """

        if not field:
            return

        slots = self.data[index]['slots']

        if field in slots:
            self.data[index]['slots'][field]['values'] = [value]
        else:
            self.data[index]['slots'][field] = {
                'token': field,
                'values': [value]
            }

    def get_slot(self, field, index=0, all_values=False):
        """
        获取槽位
        @desc 获取一个槽位slot的值
        :param field:
        :param index:
        :param all_values: 返回slot对应的所有值
        :return:
        """
        if not field:
            return ''
        return self.__get_slot_value_by_key(field, 'values', index, all_values)

    def get_slot_confirmation_status(self, field, index=0):
        """
        槽位确认状态
        :param field:
        :param index:
        :return:    NONE: 未确认；CONFIRMED: 确认；DENIED: 否认
        """

        return self.__get_slot_value_by_key(field, 'confirmationStatus', index)

    def get_intent_confirmation_status(self, index=0):
        """
        获取意图的确认状态
        :param index:
        :return:    NONE: 未确认；CONFIRMED: 确认；DENIED: 否认
        """

        return self.data[index]['confirmationStatus'] if 'confirmationStatus' in self.data[index] else ''

    def __get_slot_value_by_key(self, field, sub_field, index=0, all_values=False):
        """
        :param field:
        :param sub_field:
        :param index:
        :param all_values:
        :return:
        """

        if not ('slots' in self.data[index]):
            return ''
        slots = self.data[index]['slots']
        if field in slots:
            values = slots[field][sub_field]
            if (not all_values) and isinstance(values, list):
                values = values[0]
            return values
        else:
            return None

    def has_asked(self):
        """
        是否询问过用户,是否调用过ask
        :return:
        """

        if self.directive:
            return True
        else:
            return False

    def ask(self, slot):
        """
        询问一个特定的槽位
        :param slot:
        :return:
        """

        if slot and slot != '':
            self.ask_slot = slot
            self.directive = {
                'type': 'Dialog.ElicitSlot',
                'slotToElicit': slot,
                'updatedIntent': self.__get_update_intent()
            }
        else:
            return

    def to_directive(self):
        """
        打包NLU交互协议，返回DuerOS，为第二轮用户回答提供上下文
        在Response 中被调用
        :return:
        """
        return self.directive

    def __get_update_intent(self):
        """
        构造返回的update intent 数据结构
        :return:
        """

        if 'slots' in self.data[0]:
            return {
                'token': self.get_intent_token(),
                'slots': self.data[0]['slots'],
                'name': self.get_intent_name(),
                'confirmationStatus': self.get_intent_confirmation_status()
            }
        else:
            return {
                'token': self.get_intent_token(),
                'slots': {},
                'name': self.get_intent_name(),
                'confirmationStatus': self.get_intent_confirmation_status()
            }

    def to_update_intent(self):
        """
        bot可以修改intent中对应的值，返回给DuerOs更新
        在Response 中被调用
        :return:
        """
        return self.data[0] if self.data[0] else None

    def get_after_search_score(self):
        return self.afterSearchScore

    def set_after_search_score(self, after_search_score):
        if after_search_score and isinstance(after_search_score, float):
            self.afterSearchScore = after_search_score

    def set_delegate(self):
        """
        设置delegate 某个槽位或确认意图
        :return:
        """
        self.directive = {
            'type': 'Dialog.Delegate',
            'updatedIntent': self.__get_update_intent()
        }

    def set_confirm_slot(self, field):
        """
        设置对一个槽位的确认
        :param field:
        :return:
        """

        if 'slots' in self.data[0]:
            slots = self.data[0]['slots']
            if field in slots:
                self.directive = {
                    'type': 'Dialog.ConfirmSlot',
                    'slotToConfirm': field,
                    'updatedIntent': self.__get_update_intent()
                }

    def set_confirm_intent(self):
        """
        设置confirm 意图。询问用户是否对意图确认，设置后需要自行返回outputSpeech
        :return:
        """
        self.directive = {
            'type': 'Dialog.ConfirmIntent',
            'updatedIntent': self.__get_update_intent()
        }

    def set_select_slot_by_texts(self, slot_token, texts):
        index = 1
        options = []
        for text in texts:
            option = Option(value=text, index=index)
            index += 1
            options.append(option.__dict__)
        self.set_select_slot(slot_token, options=options)

    def set_select_slot(self, slot_token, options: list):
        """
        :param slot_token:
        :param options: list of Option
        :return:
        """
        self.directive = {
            "type": "Dialog.SelectSlot",
            "slotToSelect": slot_token,
            "updatedIntent": self.__get_update_intent(),
            "options": options
        }

    def set_select_intent(self, options: list):
        """
        :param options: list of Option
        :return:
        """
        self.directive = {
            "type": "Dialog.SelectIntent",
            "options": options
        }


class Option(object):
    def __init__(self, value,
                 entity='',
                 synonyms: list = None,
                 option_type='KEYWORD',
                 index=-1):
        self.value = value
        self.entity = entity
        self.synonyms = synonyms
        self.type = option_type
        self.index = index

    def set_index(self, index):
        self.index = index
