"""
2019.8.1 create by jun.hu
退款接口
"""

from adapay.api.request_tools import refund_create, refund_query, request_post, request_get


class Refund(object):

    @classmethod
    def create(cls, **kwargs):
        """
        发起退款流程
        """

        url = refund_create.format(kwargs.get('payment_id', ''))
        return request_post(url, kwargs)

    @classmethod
    def query(cls, **kwargs):
        """
        退款流程查询
        """

        return request_get(refund_query, kwargs)


if __name__ == '__main__':
    import logging
    import adapay
    import os
    from adapay_core.param_handler import read_file

    adapay.base_url = 'https://api-test.adapay.tech'
    adapay.config_path = os.getcwd()
    adapay.init_config('yfy_test_config', True)
    adapay.init_log(True, logging.INFO)
    adapay.public_key = read_file(adapay.config_path + '\\test_public_key.pem')


    def create_refund():
        refund = adapay.Refund.create(
            # 必填
            payment_id='002112019092011391310020965133528121344',
            refund_order_no='1568950753',
            refund_amt='0.01',
            # 可选
            reason='测试退款',
            expend={})

        print(refund)


    def query_refund():
        refund = adapay.Refund.query(
            refund_id='002112019092011391310020965133528121344')

        print(refund)


    create_refund()
    query_refund()
