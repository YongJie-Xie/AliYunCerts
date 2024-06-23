# -*- coding: utf-8 -*-
import datetime
import time

from alibabacloud_openapi_util.client import Client as OpenApiUtilClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_util import models as util_models

access_key_id = 'your_access_key_id'
access_key_secret = 'your_access_key_secret'
domains = [
    'example.com',
    'www.example.com',
]
acme_domain = 'example.com'

public_key_filepath = f'/root/.acme.sh/{acme_domain}_ecc/{acme_domain}.cer'
private_key_filepath = f'/root/.acme.sh/{acme_domain}_ecc/{acme_domain}.key'


class AliYunUtils:

    def upload_user_certificate(self, name: str, cert: str, key: str):
        config = self._get_config('cas.aliyuncs.com')
        params = self._get_params(action='UploadUserCertificate', version='2020-04-07')
        request = self._get_request({
            'Name': name,
            'Cert': cert,
            'Key': key,
        })
        response = self._get_response(config, params, request)
        return response['body']

    def set_dcdn_domain_ssl_certificate(self, domain_name: str, cert_name: str, cert_id: int):
        config = self._get_config('dcdn.aliyuncs.com')
        params = self._get_params(action='SetDcdnDomainSSLCertificate', version='2018-01-15')
        request = self._get_request({
            'DomainName': domain_name,
            'CertName': cert_name,
            'CertId': cert_id,
            'CertType': 'cas',
            'SSLProtocol': 'on',
        })
        response = self._get_response(config, params, request)
        return response['body']

    @classmethod
    def _get_config(cls, endpoint: str):
        config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
        )
        config.endpoint = endpoint
        return config

    @classmethod
    def _get_params(cls, action: str, version: str):
        params = open_api_models.Params(
            action=action,
            version=version,
            protocol='HTTPS',
            method='POST',
            auth_type='AK',
            style='RPC',
            pathname=f'/',
            req_body_type='json',
            body_type='json',
        )
        return params

    @classmethod
    def _get_request(cls, query: dict):
        request = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(query),
        )
        return request

    @classmethod
    def _get_response(cls, config, params, request):
        client = OpenApiClient(config)
        runtime = util_models.RuntimeOptions()
        response = client.call_api(params, request, runtime)
        return response


def main():
    cert_name = f'ACME_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}'
    public_key = open(public_key_filepath, 'r').read()
    private_key = open(private_key_filepath, 'r').read()

    aliyun = AliYunUtils()

    response_body = aliyun.upload_user_certificate(cert_name, public_key, private_key)
    cert_id = response_body['CertId']
    print(f'UploadUserCertificate, CertName: {cert_name}, CertId: {cert_id}')
    time.sleep(1)

    for domain in domains:
        aliyun.set_dcdn_domain_ssl_certificate(domain, cert_name, cert_id)
        print(f'SetDcdnDomainSSLCertificate, CertName: {cert_name}, Domain: {domain}')
        time.sleep(1)


if __name__ == '__main__':
    main()
