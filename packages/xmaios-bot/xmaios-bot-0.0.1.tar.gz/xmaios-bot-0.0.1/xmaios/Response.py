#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


"""
处理完后构建返回数据
详见：https://dueros.baidu.com/didp/doc/dueros-bot-platform/dbp-custom/response_markdown#response
"""
import re
from xmaios.card.TextCard import TextCard
from xmaios.directive.BaseDirective import BaseDirective
from xmaios.Base import Base
from xmaios.Utils import Utils


class Response(Base):

    def __init__(self, request, session, nlu):
        """
        :param request:
        :param session:
        :param nlu:
        """
        super(Response, self).__init__()
        self.request = request
        self.session = session
        self.nlu = nlu
        self.source_type = self.request.get_bot_id()
        self.should_end_session = True
        self.should_open_microphone = False
        self.need_determine = None
        self.expect_speech = None
        self.fallback = None
        self.expect_response = None
        self.directives_arrangement = None
        self.storage = {}

    def set_should_end_session(self, val):
        """
        设置是否结束对话, 默认结束当前会话，不支持多轮会话
        :param val: true 结束对话、 false 不结束
        :return:
        """

        if isinstance(val, bool):
            self.should_end_session = val

    def set_should_open_microphone(self, val):
        """
        设置是否开启麦克风
        :param val: True 开启麦克风、 False 不开启
        :return:
        """

        if isinstance(val, bool):
            self.should_open_microphone = val

    def update_storage(self, storage: dict):
        """
        设置存储值
        :return:
        """
        self.storage.update(storage)

    def default_result(self):

        return {
            'status': 0,
            'msg': ''
        }

    def _pre_build(self, data):
        """

        :param data:
        :return:
        """

        if self.nlu and self.nlu.has_asked():
            self.should_end_session = False

        if 'directives' not in data:
            data['directives'] = []

        if 'card' not in data:
            data['card'] = None

        if 'outputSpeech' not in data:
            data['outputSpeech'] = None

        if 'resource' not in data:
            data['resource'] = None

    def build(self, data):
        """
        构造response 返回结果
        :param data:
        data = {
            'card': card,
            'directives': directives,
            'outputSpeech': string,
            'openMicrophone': bool
        }
        :return:
        """

        if data is None:
            data = {}

        self._pre_build(data)

        directives = data['directives']

        if len(directives) > 0:
            directives = list(filter(lambda value: isinstance(value, BaseDirective), directives))
            for item in directives:
                if item.get_type() == 'DPL.ExecuteCommands':
                    item.set_token(self.get_template_token())
            directives = list(map(lambda value: value.get_data(), directives))

        if self.nlu:
            arr = self.nlu.to_directive()
            if arr:
                directives.append(arr)

        ret = {
            "version": "2.0",
            "context": self._build_context(),
            "session": self.session.to_response(),
            "response": {
                "directives":  directives,
                "shouldEndSession": self.should_end_session,
                "card": data['card'].get_data() if data['card'] else None,
                "resource": data['resource'],
                "outputSpeech": self.format_speech(data['outputSpeech']) if data['outputSpeech'] else None,
                "openMicrophone": self.should_open_microphone
            }
        }

        if isinstance(self.need_determine, bool):
            ret['response']['needDetermine'] = self.need_determine

        if isinstance(self.expect_speech, bool):
            ret['response']['expectSpeech'] = self.expect_speech

        if isinstance(self.fallback, bool):
            ret['response']['fallBack'] = self.fallback

        if self.directives_arrangement:
            ret['response']['directivesArrangement'] = self.directives_arrangement
        return ret

    def format_speech(self, mix):
        """
        通过正则 判断是纯文本还是ssml
        :param mix:
        :return:
        """
        if not mix or mix == 'null' or mix == '':
            return None

        if re.search(r'<speak>', mix):
            result = {
                "type": "SSML",
                "ssml": mix
            }
        else:
            result = {
                "type": "PlainText",
                "text": mix
            }
        return result

    def illegal_request(self):

        return {
            'status': 1,
            'msg': '非法请求'
        }

    def set_need_determine(self):

        self.need_determine = True

    def set_expect_speech(self, expect_speech=False):
        """
        通过控制expect_speech来控制麦克风开关
        :param expect_speech:
        :return:
        """
        if isinstance(expect_speech, bool):
            self.expect_speech = expect_speech

    def set_fallback(self):
        """
        表示本次返回的结果为兜底结果
        :return:
        """

        self.fallback = True

    def add_expect_text_response(self, text):
        """
        技能所期待的用户回复，技能将该信息反馈给DuerOS，有助于DuerOS在语音识别以及识别纠错时向该信息提权
        :param text:
        :return:
        """
        if text and isinstance(text, str):
            if not self.expect_response:
                self.expect_response = []
            self.expect_response.append({
                'type': 'PlainText',
                'text': text
            })

    def add_expect_slot_response(self, slot):
        """
        技能所期待的用户回复，技能将该信息反馈给DuerOS，有助于DuerOS在语音识别以及识别纠错时向该信息提权。
        :param slot:
        :return:
        """
        if slot and isinstance(slot, str):
            if not self.expect_response:
                self.expect_response = []
            self.expect_response.append({
                'type': 'Slot',
                'slot': slot
            })

    def add_expect_slot_text_response(self, slot, text):
        self.add_expect_slot_response(slot)
        self.add_expect_text_response(text)

    def _build_context(self):
        context = {'storage': self.storage}

        if self.nlu and self.nlu.to_update_intent():
            context['intent'] = self.nlu.to_update_intent()
        if self.expect_response:
            context['expectResponse'] = self.expect_response

        if self.nlu:
            after_search_score = self.nlu.get_after_search_score()
            if after_search_score and isinstance(after_search_score, float):
                context['afterSearchScore'] = after_search_score

        if not context:
            context = {}

        return context

    def set_auto_directives_arrangement(self):
        """
        表示directives中指令顺序随机
        :return:
        """
        self.directives_arrangement = 'AUTO'

    def set_strict_directives_arrangement(self):
        """
        表示directives中指令保持相对顺序不变 (directives中指令可能会被过滤)
        :return:
        """
        self.directives_arrangement = 'STRICT'

    def get_template_token(self):

        data = self.request.get_data()
        token = ''
        if data and Utils.checkKeysInDict(data, ['context', 'Screen', 'token']):
            token = Utils.get_dict_data_by_keys(data, ['context', 'Screen', 'token'])
        return token


if __name__ == '__main__':

    pass
