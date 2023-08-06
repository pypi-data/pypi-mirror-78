import unittest
from datetime import timedelta

from soapfish import soap
from soapfish.utils import timezone_offset_to_string, get_requests_ssl_context

try:
    from test.test_support import EnvironmentVarGuard
except :
    from test.support import EnvironmentVarGuard


class FormatOffsetTest(unittest.TestCase):
    def test_can_format_positive_offsets(self):
        self.assertEqual('+00:00', timezone_offset_to_string(timedelta(0)))
        self.assertEqual('+04:27', timezone_offset_to_string(timedelta(hours=4, minutes=27)))
        self.assertEqual('+14:00', timezone_offset_to_string(timedelta(hours=14)))

    def test_can_format_negative_offsets(self):
        self.assertEqual('-00:30', timezone_offset_to_string(timedelta(minutes=-30)))
        self.assertEqual('-01:30', timezone_offset_to_string(timedelta(minutes=-90)))
        self.assertEqual('-14:00', timezone_offset_to_string(timedelta(hours=-14)))


class SSLExtraContextsetTest(unittest.TestCase):

    def test_verify_false(self):
        class NoSSLCheckStub(soap.Stub):
            SERVICE = None
            SCHEME = 'https'
            HOST = 'example.com'        
            REQUESTS_CA_CHECK=False

            def __init__(*args, **kwargs):
                pass
        
        context = get_requests_ssl_context(NoSSLCheckStub())
        self.assertIn('verify', context )
        self.assertFalse(context['verify'])

    def test_environment_verify_false(self):
        context = {}
        env = EnvironmentVarGuard()
        env.set('REQUESTS_CA_CHECK', 'False')
        with env:
            context = get_requests_ssl_context()
        self.assertIn('verify', context )
        self.assertFalse(context['verify'])

    def test_provide_CA_Certs(self):

        class MyServiceStub(soap.Stub):
            SERVICE = None
            SCHEME = 'https'
            HOST = 'example.com'
            REQUESTS_CA_PATH='/path/to/ca.crt'
            REQUESTS_CERT_PATH='/path/to/certificate.crt'
            REQUESTS_KEY_PATH='/path/to/key.pem'

            def __init__(*args, **kwargs):
                pass

        context = get_requests_ssl_context(MyServiceStub())
        self.assertEqual('/path/to/ca.crt', context['verify'])
        self.assertListEqual(list(context['cert']),
            ['/path/to/certificate.crt', '/path/to/key.pem']
        )

    def test_environment_provide_CA_Certs(self):
        context={}
        env = EnvironmentVarGuard()
        env.set('REQUESTS_CA_PATH', '/path/to/ca.crt')
        env.set('REQUESTS_CERT_PATH', '/path/to/certificate.crt')
        env.set('REQUESTS_KEY_PATH', '/path/to/key.pem')
        with env:
           context = get_requests_ssl_context()
        self.assertEqual('/path/to/ca.crt', context['verify'])
        print(context['cert'])
        self.assertListEqual(list(context['cert']),
            ['/path/to/certificate.crt', '/path/to/key.pem']
        )

    def test_provide_Cert_PEM(self):
        class MyServiceStub(soap.Stub):
            SERVICE = None
            SCHEME = 'https'
            HOST = 'example.com'
            REQUESTS_CERT_PATH='/path/to/certificate.pem'

            def __init__(*args, **kwargs):
                pass

        context = get_requests_ssl_context(MyServiceStub())
        self.assertEqual('/path/to/certificate.pem', context['cert'])

    def test_environment_provide_Cert_PEM(self):
        conext={}
        env = EnvironmentVarGuard()
        env.set('REQUESTS_CERT_PATH', '/path/to/certificate.pem')
        with env:
            context = get_requests_ssl_context()
        self.assertEqual('/path/to/certificate.pem', context['cert'])


