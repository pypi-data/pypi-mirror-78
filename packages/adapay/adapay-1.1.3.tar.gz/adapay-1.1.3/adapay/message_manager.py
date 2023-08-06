import adapay
from adapay.api.request_tools import request_post, pay_message_token
from adapay_core.log_util import log_info,log_error
from adapay_core.pay_message import AdapayMessage
import os

class Connect:

    def __init__(self):
        # 长连接建立结果回调方法
        self.connect_callback = None
        # 建立监听成功回调
        self.subscribe_callback = None
        # 收到消息回调方法
        self.received_callback = None

    def set_connect_callback(self, connect_callback):
        self.connect_callback = connect_callback

    def set_subscribe_callback(self, subscribe_callback):
        self.subscribe_callback = subscribe_callback

    def set_received_callback(self, received_callback):
        self.received_callback = received_callback


    def _on_message_receiced(self, message_dict, topic):
        log_info('_on_message_receive:' + str(message_dict) + topic)
        if self.received_callback is not None:
            try:
                topic_type = topic.split("/", 2)
                if topic_type[1] and topic_type[1] == 'tokenExpireNotice':
                    log_info('已过期')
                    print('已过期')
                    self.start_connect()
                print(message_dict['type'])
                print('on_message_receive:' + str(message_dict))
                log_info('on_message_receive:' + str(message_dict))
                self.received_callback(message_dict)

            except Exception as e:
                log_error('pay message loads error:'+str(e))
                print('pay message loads error:' + str(e))


    def _on_connected(self, resp_code):
        log_info('_on_connected:' + resp_code)
        if resp_code == 0:
            print('长连接建立成功')
            log_info('connect长连接建立成功' )
        else:
            self.start_connect()
            print('长连接建立失败')
            log_info('connect长连接建立失败')
        if self.connect_callback is not None:
            try:
                self.connect_callback(resp_code)
            except Exception as e:
                print(str(e))
                log_error('长连接建立错误'+str(e))


    def _on_subscribe(self, resp_code):
        log_info('_on_subscribe:' + resp_code)
        if resp_code == 0:
            print('消息订阅成功')
            log_info('connect消息订阅成功')
        else:
            print('消息订阅失败')
            log_info('connect消息订阅失败')
        if self.subscribe_callback is not None:
            try:
                self.subscribe_callback(resp_code)
            except Exception as e:
                print(str(e))
                log_error('消息订阅错误' + str(e))


    def start_connect(self):
        expire_time = 30_000_000
        data = request_post(pay_message_token, {'expire_time': expire_time})

        if 'succeeded' != data.get('status'):
            log_info('token request failed')

        log_info('connect开始')
        ada = AdapayMessage(adapay.api_key, data.get('token', ''))
        ada.set_connect_callback(self._on_connected)
        ada.set_subscribe_callback(self._on_subscribe)
        ada.set_received_callback(self._on_message_receiced)
        ada.subscribe()
        log_info('connect结束')
        return ada



def get_message_manager():
    expire_time = 30_000_000_000
    data = request_post(pay_message_token, {'expire_time': expire_time})

    if 'succeeded' != data.get('status'):
        log_info('token request failed')

    return AdapayMessage(adapay.api_key, data.get('token', ''))
