import json

from django.contrib.auth.models import User
from pytest import mark
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
