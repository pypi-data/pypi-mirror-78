from adapay.api import request_tools
from adapay.api.request_tools import request_post


class Bill(object):

    @classmethod
    def download(cls, **kwargs):
        return request_post(request_tools.bill_download, kwargs)


if __name__ == '__main__':
    import adapay
    from adapay_core.param_handler import read_file
    import os
    import logging

    adapay.base_url = 'https://api-test.adapay.tech'
    adapay.config_path = os.getcwd()
    adapay.init_config('yfy_test_config', True)
    adapay.init_log(True, logging.INFO)
    adapay.public_key = read_file(adapay.config_path + '\\test_public_key.pem')

    download_info = adapay.Bill.download(bill_date='20190905')

    print(download_info)
