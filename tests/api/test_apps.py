from frami.api.apps import ApiConfig


def test_name():
    assert ApiConfig.name == 'api'
