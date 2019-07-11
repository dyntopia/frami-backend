import json

from django.contrib.auth.models import User
from pytest import mark, raises
from rest_framework import status


def test_index(client):
    res = client.get('/spa/')
    assert res.status_code == status.HTTP_200_OK
    assert res.content.index(b'csrfmiddlewaretoken')


@mark.django_db
def test_login(client):
    user = User.objects.create_user(username='foo', password='bar')

    res = client.post('/spa/login/', {'username': 'foo', 'password': 'xyz'})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

    res = client.post('/spa/login/', {'username': 'foo', 'password': 'bar'})
    data = json.loads(res.content.decode())
    assert data['id'] == user.id
    assert data['username'] == user.username
    assert res.status_code == status.HTTP_200_OK


@mark.django_db
def test_logout(client):
    User.objects.create_user(username='foo', password='bar')

    res = client.post('/spa/login/', {'username': 'foo', 'password': 'bar'})
    assert res.status_code == status.HTTP_200_OK

    res = client.post('/spa/logout/')
    assert res.status_code == status.HTTP_200_OK


@mark.django_db
def test_template(client):
    User.objects.create_user(username='foo', password='bar')
    User.objects.create_user(username='baz', password='qux')
    User.objects.create_user(username='abc', password='xyz')

    res = client.get('/spa/')
    with raises(ValueError):
        res.content.index(b'<script id="user" type="application/json">')

    client.login(username='baz', password='qux')
    res = client.get('/spa/')
    assert res.content.index(b'<script id="user" type="application/json">')
    assert res.content.index(b'"username": "baz"')
