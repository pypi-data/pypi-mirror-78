from adapay.api import request_tools
from adapay.api.request_tools import request_post


class User(object):

    @classmethod
    def query_union_identity(cls, **kwargs):
        return request_post(request_tools.query_identity, kwargs)


if __name__ == '__main__':
    import time
    import adapay
    from adapay_core.param_handler import read_file
    import os
    import logging

    app_id = 'app_f8b14a77-dc24-433b-864f-98a62209d6c4'

    adapay.base_url = 'https://api-test.adapay.tech'
    adapay.config_path = os.getcwd()
    adapay.init_config('yifuyun_test_config', True)
    adapay.init_log(True, logging.INFO)
    adapay.public_key = read_file(adapay.config_path + os.sep + 'test_public_key.pem')

    user_identity = adapay.User.query_union_identity(order_no=str(int(time.time())),
                                                     app_id=app_id,
                                                     user_auth_code='20190905',
                                                     app_up_identifier='20190905')

    print(user_identity)
