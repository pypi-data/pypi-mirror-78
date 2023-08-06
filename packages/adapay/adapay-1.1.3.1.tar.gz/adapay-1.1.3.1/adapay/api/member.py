from adapay.api import request_tools
from adapay.api.request_tools import request_post, request_get


class Member(object):

    @classmethod
    def create(cls, **kwargs):
        """
        创建用户
        """
        return request_post(request_tools.member_create, kwargs)

    @classmethod
    def query(cls, **kwargs):
        """
        查询用户
        """
        url = request_tools.member_query.format(member_id=kwargs.get('member_id'))
        return request_get(url, kwargs)

    @classmethod
    def query_list(cls, **kwargs):
        """
        查询用户
        """
        return request_get(request_tools.member_query_list, kwargs)

    @classmethod
    def update(cls, **kwargs):
        """
        更新用户
        """
        return request_post(request_tools.member_update, kwargs)


if __name__ == '__main__':
    import time
    import adapay
    import os
    import logging
    from adapay_core.param_handler import read_file

    app_id = 'app_f8b14a77-dc24-433b-864f-98a62209d6c4'
    # app_id = 'app_7d87c043-aae3-4357-9b2c-269349a980d6'
    adapay.base_url = 'https://api-test.adapay.tech'
    adapay.config_path = os.getcwd()
    adapay.init_config('yifuyun_test_config', True)
    adapay.init_log(True, logging.INFO)
    adapay.public_key = read_file(adapay.config_path + os.sep + 'test_public_key.pem')


    def create_member():
        # 创建用户
        member = adapay.Member.create(app_id=app_id,
                                      member_id='hf_test_member_id_account')

        print('create member resp:\n' + str(member))


    def query_member():
        # 查询用户
        member = adapay.Member.query(app_id=app_id,
                                     member_id='hf_test_member_id_account')

        print('query member resp:\n' + str(member))


    def query_member_list():
        # 查询用户列表
        member_list = adapay.Member.query_list(app_id=app_id)
        print('query member list resp:\n' + str(member_list))


    def update_member():
        # 更新用户
        import time
        timestamps_str = str(time.time())
        member = adapay.Member.update(app_id=app_id,
                                      member_id='hf_test_member_id_account',
                                      location='更新地址' + timestamps_str,
                                      email=timestamps_str + '@adapay.com',
                                      tel_no='18888888888',
                                      nickname=timestamps_str[-5:])

        print('update member resp:\n' + str(member))


    # create_member()
    query_member()
    # query_member_list()
    # update_member()
