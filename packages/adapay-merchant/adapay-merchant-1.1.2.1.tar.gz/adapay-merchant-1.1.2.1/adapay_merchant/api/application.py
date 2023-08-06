from adapay_merchant.api import request_tools
from adapay_merchant.api.request_tools import request_post, request_get


class Application(object):

    @classmethod
    def create(cls, **kwargs):
        """
        商户入驻
        """
        return request_post(request_tools.app, kwargs)

    @classmethod
    def query(cls, **kwargs):
        """
         商户入驻查询
        """
        return request_get(request_tools.app, kwargs)


if __name__ == '__main__':
    import adapay_merchant
    import logging
    import os
    from adapay_core.param_handler import read_file

    # adapay_merchant.base_url = 'https://api-test.adapay.tech'

    adapay_merchant.config_path = os.getcwd()
    adapay_merchant.init_config('dls1_test_config', True)

    adapay_merchant.init_log(True, logging.INFO)
    # adapay_merchant.public_key = read_file(adapay_merchant.config_path + '/test_public_key.pem')


    def create():
        response = adapay_merchant.Application.create(sub_api_key='api_live_fdcbcc99-4fef-4f23-a8f3-e21d7c7e4f7b',
                                                      app_name='python_test1')

        print('respose is :' + str(response))


    def query():
        response = adapay_merchant.Application.query(sub_api_key='api_live_fdcbcc99-4fef-4f23-a8f3-e21d7c7e4f7b')
        print('respose is :' + str(response))


    create()
    query()
