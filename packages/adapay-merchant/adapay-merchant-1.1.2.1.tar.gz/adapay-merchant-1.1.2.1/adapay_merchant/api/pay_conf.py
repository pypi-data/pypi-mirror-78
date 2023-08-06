from adapay_merchant.api import request_tools
from adapay_merchant.api.request_tools import request_post, request_get


class MerchantPayConf(object):
    @classmethod
    def create(cls, **kwargs):
        """
        商户入驻
        """
        return request_post(request_tools.pay_conf_create, kwargs)

    @classmethod
    def query(cls, **kwargs):
        """
         商户入驻查询
        """
        return request_get(request_tools.pay_conf_query, kwargs)

    @classmethod
    def modify(cls, **kwargs):
        """
         商户入驻修改
        """
        return request_post(request_tools.pay_conf_modify, kwargs)


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
    adapay_merchant.public_key = read_file(adapay_merchant.config_path + '\\test_public_key.pem')


    def create():
        response = adapay_merchant.MerchantPayConf.create(request_id=str(int(time.time())),
                                                          sub_api_key='api_live_826e0027-68b4-4468-ada8-aa35babdc86',
                                                          bank_channel_no='01',
                                                          app_id='app_0c2acc98-7437-4de6-ad4c-7c38a0c782e4',
                                                          wx_category='',
                                                          alipay_category='2015050700000000',
                                                          cls_id='5812',
                                                          model_type='1',
                                                          mer_type='1',
                                                          province_code='310000',
                                                          city_code='310100',
                                                          district_code='310115',
                                                          add_value_list={
                                                              'wx_lite': {'appid': '13213123123123'}
                                                          })

        print('respose is :' + str(response))


    def query():
        response = adapay_merchant.MerchantPayConf.query(request_id='1573456390')
        print('respose is :' + str(response))


    def modify():
        response = adapay_merchant.MerchantPayConf.modify(request_id=str(int(time.time())),
                                                          # 推荐商户的api_key
                                                          sub_api_key='api_live_826e0027-68b4-4468-ada8-aa35babdc86e',
                                                          alipay_request_params={
                                                              'mer_short_name': "尚云科技",
                                                              'mer_phone': "18919876721",
                                                              'fee_type': "02",
                                                              'card_no': "6227000734730752177",
                                                              'card_name': "浦发银行",
                                                              'category': "2015050700000000",
                                                              'cls_id': "5812",
                                                              'mer_name': "上海尚云科技服务有限公司",
                                                              'mer_addr': "上海市静安区",
                                                              'contact_name': "朱先生",
                                                              'contact_phone': "15866689123",
                                                              'contact_mobile': "15866689123",
                                                              'contact_email': "817888900@qq.com",
                                                              'legal_id_no': "310555196710215555",
                                                              'mer_license': "110108001111111",
                                                              'province_code': "310000",
                                                              'city_code': "310100",
                                                              'district_code': "310115"})
        print('respose is :' + str(response))


    create()
    query()
    modify()
