from adapay_merchant.api import request_tools
from adapay_merchant.api.request_tools import request_post, request_get


class MerchantUser(object):
    @classmethod
    def create(cls, **kwargs):
        """
        商户开户进件
        """
        return request_post(request_tools.merchant_user_create, kwargs)

    @classmethod
    def query(cls, **kwargs):
        """
        查询商户开户信息
        """
        return request_get(request_tools.merchant_user_query, kwargs)


if __name__ == '__main__':
    import adapay_merchant
    import time
    import logging
    import os
    from adapay_core.param_handler import read_file

    adapay_merchant.base_url = 'https://api-test.adapay.tech'
    adapay_merchant.config_path = os.getcwd()
    adapay_merchant.init_config('yfy_test_config', True)
    adapay_merchant.init_log(True, logging.INFO)
    adapay_merchant.public_key = read_file(adapay_merchant.config_path + '/test_public_key.pem')


    def create():
        response = adapay_merchant.MerchantUser.create(request_id=str(int(time.time())),
                                                       usr_phone='18888888888',
                                                       cont_name='张三',
                                                       cont_phone='16666666666',
                                                       customer_email='test@huifu.com',
                                                       mer_name='河南通达电缆股份有限公司a',
                                                       mer_short_name='河南通达电缆',
                                                       license_code='91410300X148288455',
                                                       reg_addr='reg_addr',
                                                       cust_addr='cust_addr',
                                                       cust_tel='021-88888888',
                                                       mer_start_valid_date='20190101',
                                                       mer_valid_date='20210101',
                                                       legal_name='史万福',
                                                       legal_type='0',
                                                       legal_idno='321121198606115128',
                                                       legal_mp='18888888888',
                                                       legal_start_cert_id_expires='20190101',
                                                       legal_id_expires='20210101',
                                                       card_id_mask='6227000267060250666',
                                                       bank_code='001',
                                                       card_name='中国建设银行',
                                                       bank_acct_type='2',
                                                       prov_code='1100',
                                                       area_code='0011',
                                                       rsa_public_key='016515646131sdasd1as32d13as2d13asd13')

        print('respose is :' + str(response))


    def query():
        response = adapay_merchant.MerchantUser.query(request_id='1573440302')
        print('respose is :' + str(response))


    create()
    query()
