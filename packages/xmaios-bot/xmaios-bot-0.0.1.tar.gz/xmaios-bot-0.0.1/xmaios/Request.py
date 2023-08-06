#!/usr/bin/env python3
# -*- coding=utf-8 -*-


import json
from xmaios.Nlu import Nlu
from xmaios.Session import Session
from xmaios.Utils import Utils


class Request(object):
    """
    将数据封装为Request对象, 通过Request来获取相应的请求数据
    委托Nlu、Session来解析对应数据。
    1、Nlu 处理请求数据的intent数据
    2、Session 处理请求数据的session
    """

    def __init__(self, request_data):
        """
        :param request_data:  请求数据
        """
        super(Request, self).__init__()
        if isinstance(request_data, str):
            request_data = json.loads(request_data)

        self.data = request_data
        self.request_type = self.data['request']['type']
        self.session = Session(self.data['session'])
        self.nlu = None
        if self.request_type == 'IntentRequest':
            self.nlu = Nlu(self.data['request']['intents'])
        self.arr_user_profile = None

        self._client_version = None
        self._device_type = None
        self._text = None
        self._channel = None
        self._req_type = None
        self._entry = None
        self._source = None
        # 上一轮透传信息
        self._storage = None
        # 应用信息
        self._application = None

    @property
    def channel(self) -> str:
        if self._channel is not None:
            return self._channel
        channel = Utils.get_dict_data_by_keys(self.data, ['context', 'System', 'channel'])
        if channel is None or not isinstance(channel, str):
            channel = ''
        self._channel = channel
        return self._channel

    @property
    def req_type(self) -> str:
        if self._req_type is not None:
            return self._req_type
        req_type = Utils.get_dict_data_by_keys(self.data, ['context', 'System', 'reqType'])
        if req_type is None or not isinstance(req_type, str):
            req_type = ''
        self._req_type = req_type
        return self._req_type

    @property
    def entry(self) -> str:
        if self._entry is not None:
            return self._entry
        entry = Utils.get_dict_data_by_keys(self.data, ['context', 'System', 'entry'])
        if entry is None or not isinstance(entry, str):
            entry = ''
        self._entry = entry
        return self._entry

    @property
    def source(self) -> str:
        if self._source is not None:
            return self._source
        source = Utils.get_dict_data_by_keys(self.data, ['context', 'System', 'source'])
        if source is None or not isinstance(source, str):
            source = ''
        self._source = source
        return self._source

    @property
    def application(self) -> dict:
        """
        应用配置数据
        :return:
        """
        if self._application is not None:
            return self._application
        application = Utils.get_dict_data_by_keys(self.data, ['context', 'System', 'application'])
        if application is None or not isinstance(application, dict):
            application = {}
        self._application = application
        return self._application

    @property
    def text(self) -> str:
        """
        用户原始文本输入
        :return:
        """
        if self._text is not None:
            return self._text
        text = Utils.get_dict_data_by_keys(self.data, ['request', 'query', 'original'])
        if text is None or not isinstance(text, str):
            text = ''
        self._text = text
        return self._text

    @property
    def client_version(self) -> str:
        """
        客户端版本，如8.1.0
        :return:
        """
        if self._client_version is not None:
            return self._client_version
        client_version = Utils.get_dict_data_by_keys(self.data, ['context', 'System', 'device', 'clientVersion'])
        if client_version is None or not isinstance(client_version, str):
            client_version = ''
        self._client_version = client_version
        return self._client_version

    @property
    def device_type(self) -> str:
        """
        返回设备类型
        :return: android ios
        """
        if self._device_type is not None:
            return self._device_type
        device_type = Utils.get_dict_data_by_keys(self.data, ['context', 'System', 'device', 'deviceType'])
        if device_type is None or not isinstance(device_type, str):
            device_type = ''
        self._device_type = device_type
        return self.device_type

    @property
    def storage(self) -> dict:
        if self._storage is not None:
            return self._storage
        storage = Utils.get_dict_data_by_keys(self.data, ['context', 'PrevStorage'])
        if storage is None or not isinstance(storage, dict):
            storage = {}
        self._storage = storage
        return self.storage

    def get_data(self):
        """
        返回request 请求体
        :return:
        """
        return self.data

    def get_session(self):
        """
        返回Session实例
        :return:
        """
        return self.session

    def get_nlu(self):
        """
        获取nlu实例
        :return:
        """
        return self.nlu

    def get_device_data(self) -> dict:
        """
        返回设备信息
        :return:
        """
        return Utils.get_dict_data_by_keys(self.data, ['context', 'System', 'device'])

    def get_device_id(self):
        """
        获取设备Id
        :return:
        """
        return Utils.get_dict_data_by_keys(self.data, ['context', 'System', 'device', 'deviceId'])

    def get_original_device_id(self):
        """
        获取来自端上报的原始设备Id
        :return:
        """
        return Utils.get_dict_data_by_keys(self.data, ['context', 'System', 'device', 'originalDeviceId'])

    def get_audio_player_context(self):
        """
        获取设备音频播放状态
        :return:
        """

        return Utils.get_dict_data_by_keys(self.data, ['context', 'AudioPlayer'])

    def get_video_player_context(self):
        """
        获取设备的视频播放状态
        :return:
        """

        return Utils.get_dict_data_by_keys(self.data, ['context', 'VideoPlayer'])

    def get_screen_context(self):
        """
        获取设备的屏幕信息
        :return:
        """

        return Utils.get_dict_data_by_keys(self.data, ['context', 'Screen'])

    def get_screen_token_from_context(self):
        """
        获取屏幕数据中的token
        :return:
        """

        return Utils.get_dict_data_by_keys(self.data, ['context', 'Screen', 'token'])

    def get_screen_card_from_context(self):
        """
        获取屏幕card信息
        :return:
        """
        return Utils.get_dict_data_by_keys(self.data, ['context', 'Screen', 'card'])

    def get_app_launcher_context(self):
        """
        获取设备app安装列表
        :return:
        """

        return Utils.get_dict_data_by_keys(self.data, ['context', 'AppLauncher'])

    def get_event_data(self):
        """
        获取event请求, 即请求数据的request字段数据
        非LaunchRequest会返回request字段数据
        :return:
        """

        if self.request_type == 'IntentRequest' or self.is_launch_request():
            return
        else:
            return self.data['request']

    def get_user_info(self):
        """
        获取用户信息
        :return:
        """

        return Utils.get_dict_data_by_keys(self.data, ['context', 'System', 'user', 'userInfo'])

    def get_baidu_uid(self):
        """
        获取百度Id
        :return:
        """

        return Utils.get_dict_data_by_keys(self.data,
                                           ['context', 'System', 'user', 'userInfo', 'account', 'baidu', 'baiduUid'])

    def get_type(self):
        """
        获取Request类型
        :return:
        """
        return self.request_type

    def get_user_id(self):
        """
        获取用户ID
        :return:
        """
        return Utils.get_dict_data_by_keys(self.data, ['context', 'System', 'user', 'userId'])

    def get_access_token(self):
        """
        获取accessToken
        :return:
        """
        return self._get_system_user()['accessToken']

    def _get_system_user(self):

        return Utils.get_dict_data_by_keys(self.data, ['context', 'System', 'user'])

    def get_external_access_tokens(self):
        """
        获取
        :return:
        """

        return self._get_system_user()['externalAccessTokens']

    def get_api_endpoint(self):
        """
        获取apiEndPoint
        :return:
        """
        return Utils.get_dict_data_by_keys(self.data, ['context', 'System', 'apiEndPoint'])

    def get_cuid(self):

        return self.data['cuid']

    def get_query_text(self) -> dict:
        """
        获取请求的Query
        :return: {'type': 'TEXT' , 'original': ''}
        """
        return Utils.get_dict_data_by_keys(self.data, ['request', 'query', 'text'])

    def get_location(self):
        """
        获取设备位置信息
        :return:
        """
        if self._get_system_user()['userInfo']['location']:
            return self._get_system_user()['userInfo']['location']

    def is_determined(self):

        if self.request_type == 'IntentRequest' and Utils.get_dict_data_by_keys(self.data, ['request', 'determined']):
            return Utils.get_dict_data_by_keys(self.data, ['request', 'determined'])
        else:
            return False

    def is_launch_request(self):
        """
        是否为调起bot LaunchRequest 请求
        :return:
        """
        return self.data['request']['type'] == 'LaunchRequest'

    def is_session_end_request(self):
        """
        是否关闭bot请求
        :return:
        """
        return self.data['request']['type'] == 'SessionEndedRequest'

    def is_session_ended_request(self):
        """
        判断是否是结束会话
        :return:
        """
        return self.is_session_end_request()

    def get_timestamp(self):

        return Utils.get_dict_data_by_keys(self.data, ['request', 'timestamp'])

    def get_log_id(self):

        return Utils.get_dict_data_by_keys(self.data, ['request', 'requestId'])

    def get_bot_id(self):

        return Utils.get_dict_data_by_keys(self.data, ['context', 'System', 'application', 'applicationId'])

    def is_dialog_state_completed(self):
        """
        槽位是否填完

        :return:
        """
        return self.data['request']['dialogState'] == 'COMPLETED'

    def get_supported_interfaces(self):

        return Utils.get_dict_data_by_keys(self.data, ['context', 'System', 'device', 'supportedInterfaces'])

    def get_api_access_token(self):
        """
        获取ApiAccessToken  申请授权的时候使用
        :return:
        """
        return Utils.get_dict_data_by_keys(self.data, ['context', 'System', 'apiAccessToken'])

    def get_support_video_player(self):
        interfaces = self.get_supported_interfaces()
        return Utils.getDictDataByKey(interfaces, 'VideoPlayer')

    def get_support_video_player_prefered_bitrate(self):
        video_player = self.get_support_video_player()
        if video_player:
            if 'preferedBitrate' in video_player:
                return video_player['preferedBitrate']
        else:
            return ''


if __name__ == '__main__':
    pass
