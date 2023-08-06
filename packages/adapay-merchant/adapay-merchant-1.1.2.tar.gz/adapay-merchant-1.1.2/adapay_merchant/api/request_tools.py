# url path 统一管理 花括号中变量代表待替换值
import adapay_merchant
from adapay_core import ApiRequest

pay_message_token = '/v1/token/apply'

# ----------merchant_user----------
merchant_user_create = '/v1/batchEntrys/userEntry'
merchant_user_query = '/v1/batchEntrys/userEntry'

# ----------pay_conf----------
pay_conf_create = '/v1/batchInput/merConf'
pay_conf_query = '/v1/batchInput/merConf'
pay_conf_modify = '/v1/batchInput/merResidentModify'

# ----------merchant_profile----------
profile_audit = '/v1/merProfile/merProfileForAudit'
profile_picture = '/v1/merProfile/merProfilePicture'
profile_status = '/v1/merProfile/merProfile'

# application
app = '/v1/batchEntrys/application'


def __request_init(url, request_params):
    ApiRequest.base_url = adapay_merchant.base_url
    ApiRequest.build(adapay_merchant.api_key, adapay_merchant.private_key, adapay_merchant.public_key, url,
                     request_params, adapay_merchant.__version__, adapay_merchant.connect_timeout)


def request_post(url, request_params, files=None):
    __request_init(url, request_params)
    return ApiRequest.post(files)


def request_get(url, request_params):
    __request_init(url, request_params)
    return ApiRequest.get()
