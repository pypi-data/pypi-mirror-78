"""
2019.8.1 create by jun.hu
默认请求对象
"""
import json

import requests

from adapay_core.log_util import log_error, log_info
from adapay_core.param_handler import pop_empty_value, get_plain_text
from adapay_core.rsa_utils import rsa_sign, rsa_design


class ApiRequest:
    base_url = ''
    url = ''
    api_key = ''
    request_params = {}
    version = ''
    private_key = ''
    public_key = ''
    connect_timeout = ''

    @staticmethod
    def build(api_key, private_key, public_key, url, request_params, version, connect_timeout=30):
        ApiRequest.url = url
        ApiRequest.api_key = api_key
        ApiRequest.private_key = private_key
        ApiRequest.public_key = public_key
        ApiRequest.request_params = request_params
        ApiRequest.version = version
        ApiRequest.connect_timeout = connect_timeout

    @staticmethod
    def post(request_file=None):
        return ApiRequest._request('post', request_file)

    @staticmethod
    def get():
        return ApiRequest._request('get')

    @staticmethod
    def _build_request_info(url, method, params, files):
        """
        根据请求方式构造请求头和请求参数
        :return: header 请求头 params 请求参数
        """
        # 构造请求头
        header = {'authorization': ApiRequest.api_key,
                  "sdk_version": 'python_v' + ApiRequest.version,
                  'signature': ''}

        params = pop_empty_value(params)

        plain_text = url

        # 根据不通方法进行不同加签处理
        if params:
            if 'post' == method and not files:
                plain_text = plain_text + json.dumps(params)
            else:
                plain_text = plain_text + get_plain_text(params)

        # 获取商户密钥
        if not ApiRequest.private_key:
            raise RuntimeError('privite_key is none')

        # 对请求参数进行加签
        flag, cipher_text = rsa_sign(ApiRequest.private_key, plain_text, 'utf-8')

        if not flag:
            log_error('request to {}, sign error {} '.format(url, cipher_text))

        # 将签名更新到请求头中
        header.update({'signature': cipher_text})
        log_info('request to {}, param is {}, \nhead is {}'.format(url, params, header))

        return header, params

    @staticmethod
    def _request(method, files=None):
        """
        执行请求
        :param method: 请求方法类型

        :param files: 上传的文件
        :return: 网路请求返回的数据
        """

        request_url = ApiRequest.base_url + ApiRequest.url

        header, params = ApiRequest._build_request_info(request_url, method, ApiRequest.request_params, files)

        http_method = getattr(requests, method or 'post')

        if files:
            resp = http_method(request_url, data=params, files=files, timeout=ApiRequest.connect_timeout,
                               headers=header)

        elif method == 'post':
            resp = http_method(request_url, json=params, files=files, timeout=ApiRequest.connect_timeout,
                               headers=header)

        else:
            resp = http_method(request_url, params, timeout=ApiRequest.connect_timeout, headers=header)

        log_info('request to {}, resp is {}'.format(request_url, resp.text))

        return ApiRequest._build_return_data(resp)

    @staticmethod
    def _build_return_data(resp):

        try:
            resp_json = json.loads(resp.text)
        except Exception as e:
            log_error('adapay resp_code is ' + str(resp.status_code))
            log_error(str(e))
            return resp.text

        # 服务端返回数据
        data = resp_json.get('data', '')
        # 返回字段中的签名
        resp_sign = resp_json.get('signature', '')

        if not resp_sign:
            # 如果没有签名字段，直接返回内容，一般为404等
            return resp_json

        # 当业务请求成功时验证返回数据与签名
        if not ApiRequest.public_key:
            raise RuntimeError('public_key is none')

        # 验证返回数据与返回加签结果是否一致
        flag, info = rsa_design(resp_sign, data, ApiRequest.public_key)

        if not flag:
            # 如果验签失败，抛出异常
            log_error('check signature error !'.format(info))
            raise RuntimeError(info)

        return json.loads(data)
