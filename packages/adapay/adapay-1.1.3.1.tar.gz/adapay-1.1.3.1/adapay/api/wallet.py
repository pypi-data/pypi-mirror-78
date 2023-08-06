# import sys
# sys.path.append("../../..")
from adapay.api import request_tools
from adapay.api.request_tools import request_post, request_get


class Wallet(object):
    #  这里的域名与 adapay 支付区分开
    wallet_base_url = 'https://page.adapay.tech'

    @classmethod
    def login(cls, **kwargs):
        """
        钱包用户登录
        :param kwargs:
        :return:
        """
        return request_post(request_tools.wallet_login, kwargs, base_url=Wallet.wallet_base_url)

    @classmethod
    def pay(cls, **kwargs):
        """
        钱包支付
        :param kwargs:
        :return:
        """
        return request_post(request_tools.wallet_pay, kwargs, base_url=Wallet.wallet_base_url)

    @classmethod
    def checkout(cls, **kwargs):
        """
        创建收银台对象
        :param kwargs:
        :return:
        """
        return request_post(request_tools.wallet_checkout, kwargs, base_url=Wallet.wallet_base_url)

    @classmethod
    def checkout_list(cls, **kwargs):
        """
        创建收银台对象
        :param kwargs:
        :return:
        """
        return request_get(request_tools.wallet_checkout_list, kwargs, base_url=Wallet.wallet_base_url)


if __name__ == '__main__':
    import adapay
    import logging
    import os
    from adapay_core.param_handler import read_file

    # app_id = 'app_f8b14a77-dc24-433b-864f-98a62209d6c4'
    app_id = 'app_7d87c043-aae3-4357-9b2c-269349a980d6'
    # adapay.config_path = os.getcwd()
    d = os.path.dirname(__file__)  # 返回当前文件所在的目录
    parent_path = os.path.dirname(d)
    # dirname, filename = os.path.split(os.path.abspath(__file__))
    sep = os.sep
    config_path = parent_path + sep + 'config'
    adapay.config_path = config_path
    adapay.init_config("yifuyun_config", True)


    # adapay.public_key = read_file(adapay.config_path + os.sep + 'test_public_key.pem')

    def wallet_login():
        login_result = adapay.Wallet.login(app_id=app_id,
                                           member_id='0',
                                           ip='127.0.0.1')
        print(login_result)


    def wallet_pay():
        import time

        pay_result = adapay.Wallet.pay(app_id=app_id,
                                       order_no=str(int(time.time())),
                                       pay_amt='0.01',
                                       goods_title='测试商品',
                                       goods_desc='测试商品描述')
        print(pay_result)


    def wallet_checkout():
        import time

        result = adapay.Wallet.checkout(order_no=str(int(time.time())),
                                        app_id=app_id,
                                        member_id='user_00013',
                                        pay_amt='0.01',
                                        currency='cny',
                                        goods_title='测试商品',
                                        goods_desc='测试商品描述',
                                        callback_url='https://www.baidu.com')
        print(result)

    def wallet_checkout_list():
        import time

        result = adapay.Wallet.checkout_list(order_no=str(int(time.time())),
                                        app_id=app_id,
                                        member_id='user_00013')
        print(result)

    # wallet_login()
    # wallet_pay()
    # wallet_checkout()
    # wallet_checkout_list()
