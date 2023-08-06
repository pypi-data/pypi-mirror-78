from adapay_merchant.api import request_tools
from adapay_merchant.api.request_tools import request_post, request_get
import os


class MerchantProfile(object):

    @classmethod
    def mer_profile_picture(cls, **kwargs):
        """
        代理商（渠道商）上送商户证照
        :param kwargs:
        :return:
        """

        file_path = kwargs.get('file')
        file_dict = {'file': (os.path.basename(file_path), open(file_path, 'rb'), 'application/octet-stream')}
        kwargs.pop('file')
        return request_post(request_tools.profile_picture, kwargs, file_dict)

    @classmethod
    def mer_profile_for_audit(cls, **kwargs):
        """
        代理商（渠道商）将商户证照信息提交审核接口
        :param kwargs:
        :return:
        """

        return request_post(request_tools.profile_audit, kwargs)

    @classmethod
    def query_mer_profile_status(cls, **kwargs):
        """
        查询商户基础信息审核状态
        :param kwargs:
        :return:
        """

        return request_get(request_tools.profile_status, kwargs)


if __name__ == '__main__':
    import adapay_merchant
    import time
    import logging
    from adapay_core.param_handler import read_file

    # adapay_merchant.base_url = 'https://api-test.adapay.tech'
    adapay_merchant.config_path = os.getcwd()
    adapay_merchant.init_config('yifuyun_config', True)
    adapay_merchant.init_log(True, logging.INFO)


    # adapay_merchant.public_key = read_file(adapay_merchant.config_path + '\\test_public_key.pem')

    def picture():
        response = adapay_merchant.MerchantProfile.mer_profile_picture(
            subApiKey='api_live_fdcbcc99-4fef-4f23-a8f3-e21d7c7e4f7b',
            file='./yifuyun_config.json',
            fileType='01')
        print('respose is :' + str(response))


    def audit():
        response = adapay_merchant.MerchantProfile.mer_profile_for_audit(
            subApiKey='api_live_fdcbcc99-4fef-4f23-a8f3-e21d7c7e4f7b',
            socialCreditCodeId='0067363309554112',
            legalCertIdFrontId='0067363504549376',
            legalCertIdBackId='0067363574467008',
            businessAdd='http://www.baidu.com',
            storeId='0067361944316352|0067363749735936',
            accountOpeningPermitId='0067364019530176')

        print('respose is :' + str(response))


    def query_status():
        response = adapay_merchant.MerchantProfile.query_mer_profile_status(
            subApiKey='api_live_fdcbcc99-4fef-4f23-a8f3-e21d7c7e4f7b')

        print('respose is :' + str(response))


    # picture()
    # audit()
    query_status()
