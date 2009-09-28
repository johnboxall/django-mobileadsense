from django.core.handlers.wsgi import WSGIRequest
from django.template import Template, Context
from django.test import TestCase, Client
from adsense import adsense

class RequestFactory(Client):
    def request(self, **request):
        environ = {
            'HTTP_COOKIE': self.cookies,
            'PATH_INFO': '/',
            'QUERY_STRING': '',
            'REQUEST_METHOD': 'GET',
            'SCRIPT_NAME': '',
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': 80,
            'SERVER_PROTOCOL': 'HTTP/1.1',
        }
        environ.update(self.defaults)
        environ.update(request)
        return WSGIRequest(environ)

test_request_params = {
    "USER_AGENT": "AdSense Tester",
    "REMOTE_ADDR": "127.0.0.1"
}
test_request = RequestFactory(**test_request_params).get("/")
test_publisher_id = "pub-5889931444784070"

class TestAdSense(TestCase):
    def test_adsense(self):
        response = adsense(test_request, test_publisher_id)
        self.assertTrue(len(response))
    
class TemplateTagTest(TestCase):
    def test_mobileadsense(self):
        t = Template('{% load adsense_tags %}{% mobileadsense "pub-5889931444784070" %}')
        c = Context({"request": test_request})
        response = t.render(c)
        self.assertTrue(len(response))