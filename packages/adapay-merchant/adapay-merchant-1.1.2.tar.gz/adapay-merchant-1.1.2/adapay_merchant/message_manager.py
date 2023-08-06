import adapay_merchant
from adapay_core.log_util import log_info
from adapay_core.pay_message import AdapayMessage
from adapay_merchant.api.request_tools import request_post, pay_message_token


def get_message_manager():
    expire_time = 30_000_000_000
    data = request_post(pay_message_token, {'expire_time': expire_time})

    if 'succeeded' != data.get('status'):
        log_info('token request failed')

    return AdapayMessage(adapay_merchant.api_key, data.get('token', ''))
