from django.contrib.auth.models import User
from pytest import mark


@mark.django_db
def test_unauthenticated(client):
    user = User.objects.create_user(username='foo', password='bar')
    assert client.get('/api/user/').status_code == 403
    assert client.get('/api/user/{}/'.format(user.id)).status_code == 403


@mark.django_db
def test_list(client):
    user = User.objects.create_user(username='foo', password='bar')
    staff = User.objects.create_user(username='x', password='y', is_staff=True)

    client.login(username='foo', password='bar')
    res = client.get('/api/user/')
    assert res.status_code == 403

    client.login(username='x', password='y')
    res = client.get('/api/user/')
    assert res.status_code == 200
    assert len(res.data) == 2
    assert res.data[0]['id'] == user.id
    assert res.data[1]['id'] == staff.id


@mark.django_db
def test_retrieve(client):
    user = User.objects.create_user(username='foo', password='bar')

    client.login(username='foo', password='bar')
    res = client.get('/api/user/{}/'.format(user.id))
    assert res.status_code == 200
    assert res.data['id'] == user.id
    assert res.data['username'] == user.username


@mark.django_db
def test_retrieve_other(client):
    User.objects.create_user(username='foo', password='bar')
    user = User.objects.create_user(username='baz', password='qux')
    User.objects.create_user(username='x', password='y', is_staff=True)

    client.login(username='foo', password='bar')
    res = client.get('/api/user/{}/'.format(user.id))
    assert res.status_code == 403

    client.login(username='x', password='y')
    res = client.get('/api/user/{}/'.format(user.id))
    assert res.status_code == 200
    assert res.data['id'] == user.id
    assert res.data['username'] == user.username
