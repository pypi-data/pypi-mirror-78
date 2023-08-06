"""
2019.8.1 create by yumin.chang
调用支付接口
"""
from adapay.api.request_tools import payment_create, payment_query, payment_list, payment_close, payment_reverse, \
    payment_reverse_query_list, payment_confirm, payment_confirm_query, payment_confirm_query_list, \
    payment_reverse_query, request_post, request_get


class Payment(object):

    @classmethod
    def create(cls, **kwargs):
        """
        创建订单
        """
        if not kwargs.get('currency'):
            kwargs['currency'] = 'cny'

        return request_post(payment_create, kwargs)

    @classmethod
    def create_confirm(cls, **kwargs):
        """
        创建订单确认
        """
        return request_post(payment_confirm, kwargs)

    @classmethod
    def query_confirm(cls, **kwargs):
        """
        查询订单确认
        """
        url = payment_confirm_query.format(payment_confirm_id=kwargs.get('payment_confirm_id'))
        return request_get(url, kwargs)

    @classmethod
    def query_confirm_list(cls, **kwargs):
        """
         查询订单确认列表
        """
        return request_get(payment_confirm_query_list, kwargs)

    @classmethod
    def create_reverse(cls, **kwargs):
        """
        支付撤销
        """
        return request_post(payment_reverse, kwargs)

    @classmethod
    def query_reverse(cls, **kwargs):
        """
        查询支付撤销
        """
        url = payment_reverse_query.format(reverse_id=kwargs.get('reverse_id'))
        return request_get(url, kwargs)

    @classmethod
    def query_reverse_list(cls, **kwargs):
        """
        查询支付撤销列表
        """
        return request_get(payment_reverse_query_list, kwargs)

    @classmethod
    def query(cls, **kwargs):
        """
        支付查询
        """
        url = payment_query.format(payment_id=kwargs.get('payment_id'))
        return request_get(url, kwargs)

    @classmethod
    def list(cls, **kwargs):
        """
        支付查询
        """
        return request_get(payment_list, kwargs)

    @classmethod
    def close(cls, **kwargs):
        """
        关单请求
        """
        url = payment_close.format(kwargs['payment_id'])
        return request_post(url, kwargs)


if __name__ == '__main__':
    import time
    import logging
    import adapay
    import os
    from adapay_core.param_handler import read_file

    # app_id = 'app_f8b14a77-dc24-433b-864f-98a62209d6c4'
    # # app_id = 'app_7d87c043-aae3-4357-9b2c-269349a980d6'
    # adapay.base_url = 'https://api-test.adapay.tech'
    # adapay.config_path = os.getcwd()
    # adapay.init_config('yifuyun_test_config', True)
    # adapay.init_log(True, logging.INFO)
    # adapay.public_key = read_file(adapay.config_path + os.sep + 'test_public_key.pem')
    order_no = str(int(time.time()))

    app_id = 'app_7d87c043-aae3-4357-9b2c-269349a980d6'
    # adapay.config_path = os.getcwd()
    d = os.path.dirname(__file__)  # 返回当前文件所在的目录
    parent_path = os.path.dirname(d)
    # dirname, filename = os.path.split(os.path.abspath(__file__))
    sep = os.sep
    config_path = parent_path + sep + 'config'
    adapay.config_path = config_path
    adapay.init_config("yifuyun_config", True)


    def create_payment():
        payment = adapay.Payment.create(order_no=order_no,
                                        app_id=app_id,
                                        pay_channel='alipay_qr',
                                        pay_amt='0.01',
                                        goods_title='goods_title',
                                        goods_desc='goods_desc',
                                        pay_mode='delay'
                                        # 如果需要分账
                                        # div_members=[{'member_id': 'corp_1243432427',
                                        #               'amount': '0.01',
                                        #               'fee_flag': 'Y'}]
                                        )

        print(payment)


    def confirm_create():
        payment = adapay.Payment.create_confirm(payment_id='002112019102217024710032642976114446336',
                                                order_no='1571734967',
                                                confirm_amt='0.01')
        print(payment)


    def query_confirm():
        payment = adapay.Payment.query_confirm(payment_confirm_id='002112019101416035700029729065277411328')
        print(payment)


    def query_confirm_list():
        payment = adapay.Payment.query_confirm_list(app_id=app_id,
                                                    created_gte='1571734200000',
                                                    created_lte='1571738400000')
        print(payment)


    def reverse_payment():
        payment = adapay.Payment.create_reverse(payment_id='002112019102219102610032675098410516480',
                                                app_id=app_id,
                                                order_no='1571742626',
                                                reverse_amt='0.01')
        print(payment)


    def query_reverse():
        payment = adapay.Payment.query_reverse(reverse_id='002112019102219134810032675945551794176')
        print(payment)


    def query_reverse_list():
        payment = adapay.Payment.query_reverse_list(app_id=app_id)
        print(payment)


    def query_payment():
        query_result = adapay.Payment.query(payment_id='002112019102219102610032675098410516480')
        print(query_result)

    def query_list():
        list_result = adapay.Payment.list(app_id=app_id,
                                          order_no='1571742626',
                                          payment_id='002112019102219102610032675098410516480')
        print(list_result)

    def close_payment():
        close_result = adapay.Payment.close(payment_id='002112019092011295210020962782647078912',
                                            # 非必填
                                            description='close_test',
                                            extra={'test_key': 'test_value'})
        print(close_result)


    # create_payment()
    # confirm_create()
    # query_confirm()
    # query_confirm_list()
    # reverse_payment()
    # query_reverse()
    # query_reverse_list()
    # query_payment()
    # close_payment()
    # query_list()
