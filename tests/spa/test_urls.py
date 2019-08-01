from importlib import reload

from pytest import raises

import frami.spa.urls


def test_email(mocker):
    settings = mocker.patch('django.conf.settings')
    settings.EMAIL_HOST = 'foo'
    settings.EMAIL_HOST_USER = 'bar'
    settings.EMAIL_HOST_PASSWORD = 'baz'
    settings.EMAIL_PORT = 123
    settings.EMAIL_USE_TLS = True

    reload(frami.spa.urls)
    urlpatterns = frami.spa.urls.urlpatterns
    assert next(x for x in urlpatterns if x.name == 'password_reset')


def test_no_email(mocker):
    settings = mocker.patch('django.conf.settings')
    settings.EMAIL_HOST = 'foo'
    settings.EMAIL_HOST_USER = 'bar'
    settings.EMAIL_HOST_PASSWORD = 'baz'
    settings.EMAIL_PORT = 123
    settings.EMAIL_USE_TLS = False

    reload(frami.spa.urls)
    urlpatterns = frami.spa.urls.urlpatterns
    with raises(StopIteration):
        next(x for x in urlpatterns if x.name == 'password_reset')
