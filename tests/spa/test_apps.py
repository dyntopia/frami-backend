from frami.spa.apps import SpaConfig


def test_name():
    assert SpaConfig.name == 'spa'
