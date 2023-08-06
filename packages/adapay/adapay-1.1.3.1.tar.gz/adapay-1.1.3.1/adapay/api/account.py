from adapay.api import request_tools
from adapay.api.request_tools import request_post, request_get


class Account(object):

    @classmethod
    def create_settle(cls, **kwargs):
        """
        创建结算账户
        """
        return request_post(request_tools.settle_account_create, kwargs)

    @classmethod
    def query_settle(cls, **kwargs):
        """
        查询结算账户
        """
        url = request_tools.settle_account_query.format(settle_account_id=kwargs.get('settle_account_id'))
        return request_get(url, kwargs)

    @classmethod
    def modify_settle(cls, **kwargs):
        """
        修改结算配置
        """
        return request_post(request_tools.settle_account_modify, kwargs)

    @classmethod
    def delete_settle(cls, **kwargs):
        """
        删除结算账户
        """
        return request_post(request_tools.settle_account_delete, kwargs)

    @classmethod
    def query_settle_details(cls, **kwargs):
        """
        查询结算账户明细
        """
        return request_get(request_tools.settle_account_detail_query, kwargs)

    @classmethod
    def query_balance(cls, **kwargs):
        """
        查询账户余额
        """
        return request_get(request_tools.settle_account_balance_query, kwargs)

    @classmethod
    def draw_cash(cls, **kwargs):
        """
        取现
        """
        return request_post(request_tools.settle_account_cash_draw, kwargs)

    @classmethod
    def query_draw_cash_status(cls, **kwargs):
        """
        取现状态查询
        """
        return request_get(request_tools.cash_draw_status, kwargs)


if __name__ == '__main__':
    import time
    import adapay
    from adapay_core.param_handler import read_file
    import os
    import logging

    order_no = str(int(time.time()))
    # app_id = 'app_f8b14a77-dc24-433b-864f-98a62209d6c4'
    app_id = 'app_7d87c043-aae3-4357-9b2c-269349a980d6'
    # adapay.base_url = 'https://api-test.adapay.tech'
    adapay.config_path = os.getcwd()
    adapay.init_config('yifuyun_config', True)
    # adapay.init_config('hf_test_config', True)
    adapay.init_log(True, logging.INFO)


    # adapay.public_key = read_file(adapay.config_path + '\\test_public_key.pem')

    def create_settle():
        settle_account = adapay.Account.create_settle(app_id=app_id,
                                                      member_id='hf_test_member_id_account',
                                                      channel='bank_account',
                                                      account_info={
                                                          'card_id': '6227000267060250576',
                                                          'card_name': '常昱旻',
                                                          'cert_type': '00',
                                                          'cert_id': '140106199203200631',
                                                          'tel_no': '13754892205',
                                                          'bank_code': '0105999',
                                                          'bank_acct_type': '2',
                                                          'prov_code': '0014',
                                                          'area_code': '1401'
                                                      })
        print('create settle account is \n' + str(settle_account))


    def query_settle():
        settle_account = adapay.Account.query_settle(app_id=app_id,
                                                     member_id='hf_test_member_id_account',
                                                     settle_account_id='0006440476699456')
        print('query settle account is \n' + str(settle_account))


    def modify_settle():
        settle_account = adapay.Account.modify_settle(app_id=app_id,
                                                      member_id='user_test_10001',
                                                      settle_account_id='0023056905335360',
                                                      min_amt='0.01',
                                                      remained_amt='0.01')
        print('modify settle account is \n' + str(settle_account))


    def delete_settle():
        settle_account = adapay.Account.delete_settle(app_id=app_id,
                                                      member_id='hf_test_member_id_account',
                                                      settle_account_id='0006440476699456')

        print('delete settle account is \n' + str(settle_account))


    def query_settle_detail():
        settle_account = adapay.Account.query_settle_details(app_id=app_id,
                                                             member_id='0',
                                                             begin_date='20190908',
                                                             end_date='20191009')

        print('query settle detail is \n' + str(settle_account))


    def query_balance():
        settle_account = adapay.Account.query_balance(app_id=app_id,
                                                      member_id='user_00008',
                                                      settle_account_id='0035172521665088')

        print('query balance detail is \n' + str(settle_account))


    def draw_cash():
        settle_account = adapay.Account.draw_cash(order_no=order_no,
                                                  app_id=app_id,
                                                  cash_type='T1',
                                                  cash_amt='0.02',
                                                  member_id='user_00008',
                                                  notify_url='https://www.baidu.com')

        print('draw cash detail is \n' + str(settle_account))


    def query_draw_cash_status():
        settle_account = adapay.Account.query_draw_cash_status(order_no='jdskjdd_14142124567')
        print('draw cash status is \n' + str(settle_account))


    # create_settle()
    # query_settle()
    # modify_settle()
    # delete_settle()
    # query_settle_detail()
    # query_balance()
    # draw_cash()
    query_draw_cash_status()
