# url path 统一管理 花括号中变量代表待替换值
import adapay
from adapay_core import ApiRequest

pay_message_token = '/v1/token/apply'

# ----------payment 对象----------
payment_create = '/v1/payments'
payment_confirm = '/v1/payments/confirm'
payment_confirm_query = '/v1/payments/confirm/{payment_confirm_id}'
payment_confirm_query_list = '/v1/payments/confirm/list'
payment_reverse = '/v1/payments/reverse'
payment_reverse_query = '/v1/payments/reverse/{reverse_id}'
payment_reverse_query_list = '/v1/payments/reverse/list'
payment_query = '/v1/payments/{payment_id}'
payment_close = '/v1/payments/{}/close'
payment_list = '/v1/payments/list'

# ----------refund 对象----------
refund_create = '/v1/payments/{}/refunds'
refund_query = '/v1/payments/refunds'

# ----------bill 账单----------
bill_download = '/v1/bill/download'

# ----------member 对象 ----------
member_create = '/v1/members'
member_query = '/v1/members/{member_id}'
member_query_list = '/v1/members/list'
member_update = '/v1/members/update'
corp_member_create = '/v1/corp_members'
corp_member_query = '/v1/corp_members/{member_id}'

# ----------account 对象 ----------
settle_account_create = '/v1/settle_accounts'
settle_account_modify = '/v1/settle_accounts/modify'
settle_account_query = '/v1/settle_accounts/{settle_account_id}'
settle_account_delete = '/v1/settle_accounts/delete'
settle_account_detail_query = '/v1/settle_accounts/settle_details'
settle_account_balance_query = '/v1/settle_accounts/balance'
settle_account_cash_draw = '/v1/cashs'
cash_draw_status = '/v1/cashs/stat'

# ----------user 对象 ----------
query_identity = '/v1/union/user_identity'

# ----------wallet 对象 ----------
wallet_login = '/v1/walletLogin'
wallet_pay = '/v1/account/payment'
wallet_checkout = '/v1/checkout'
wallet_checkout_list = '/v1/checkout/list'


# 这里外部传入url，目前存在多个base_url
def __request_init(url, request_params, base_url):
    ApiRequest.base_url = base_url if base_url else adapay.base_url
    ApiRequest.build(adapay.api_key, adapay.private_key, adapay.public_key, url, request_params, adapay.__version__,
                     adapay.connect_timeout)


def request_post(url, request_params, files=None, base_url=''):
    __request_init(url, request_params, base_url)
    return ApiRequest.post(files)


def request_get(url, request_params, base_url=''):
    __request_init(url, request_params, base_url)
    return ApiRequest.get()
