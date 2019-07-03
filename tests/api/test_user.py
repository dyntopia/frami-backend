from django.contrib.auth.models import User
from pytest import mark
from rest_framework import status


@mark.django_db
def test_unauthenticated(client):
    user = User.objects.create_user(username='foo', password='bar')
    assert client.get('/api/user/').status_code == status.HTTP_403_FORBIDDEN
    assert client.get('/api/user/{}/'.format(user.id)).status_code == \
        status.HTTP_403_FORBIDDEN


@mark.django_db
def test_create(client):
    User.objects.create_user(username='foo', password='bar')
    User.objects.create_user(username='x', password='y', is_staff=True)

    client.login(username='foo', password='bar')
    res = client.post('/api/user/', {'username': 'abc'})
    assert res.status_code == status.HTTP_403_FORBIDDEN

    client.login(username='x', password='y')
    res = client.post('/api/user/', {'username': 'abc'})
    assert not res.data['is_staff']
    assert res.data['username'] == 'abc'
    assert res.status_code == status.HTTP_201_CREATED

    client.login(username='x', password='y')
    res = client.post('/api/user/', {'username': 'xyz', 'is_staff': True})
    assert res.data['is_staff']
    assert res.data['username'] == 'xyz'
    assert res.status_code == status.HTTP_201_CREATED


@mark.django_db
def test_destroy(client):
    user = User.objects.create_user(username='foo', password='bar')
    other = User.objects.create_user(username='abc', password='def')
    staff = User.objects.create_user(username='x', password='y', is_staff=True)

    user_url = '/api/user/{}/'.format(user.id)
    other_url = '/api/user/{}/'.format(other.id)
    staff_url = '/api/user/{}/'.format(staff.id)

    # User delete other.
    client.login(username='foo', password='bar')
    assert client.delete(other_url).status_code == status.HTTP_403_FORBIDDEN

    # User delete self.
    client.login(username='foo', password='bar')
    assert client.delete(user_url).status_code == status.HTTP_403_FORBIDDEN

    # Staff delete other.
    client.login(username='x', password='y')
    assert client.delete(other_url).status_code == status.HTTP_204_NO_CONTENT
    assert client.get(other_url).status_code == status.HTTP_404_NOT_FOUND

    # Staff delete self.
    assert client.delete(staff_url).status_code == status.HTTP_204_NO_CONTENT
    assert client.get(staff_url).status_code == status.HTTP_403_FORBIDDEN


@mark.django_db
def test_list(client):
    user = User.objects.create_user(username='foo', password='bar')
    staff = User.objects.create_user(username='x', password='y', is_staff=True)

    client.login(username='foo', password='bar')
    res = client.get('/api/user/')
    assert res.status_code == status.HTTP_403_FORBIDDEN

    client.login(username='x', password='y')
    res = client.get('/api/user/')
    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 2
    assert res.data[0]['id'] == user.id
    assert res.data[1]['id'] == staff.id


@mark.django_db
def test_retrieve(client):
    user = User.objects.create_user(username='foo', password='bar')

    client.login(username='foo', password='bar')
    res = client.get('/api/user/{}/'.format(user.id))
    assert res.status_code == status.HTTP_200_OK
    assert res.data['id'] == user.id
    assert res.data['username'] == user.username


@mark.django_db
def test_retrieve_other(client):
    User.objects.create_user(username='foo', password='bar')
    user = User.objects.create_user(username='baz', password='qux')
    User.objects.create_user(username='x', password='y', is_staff=True)

    client.login(username='foo', password='bar')
    res = client.get('/api/user/{}/'.format(user.id))
    assert res.status_code == status.HTTP_403_FORBIDDEN

    client.login(username='x', password='y')
    res = client.get('/api/user/{}/'.format(user.id))
    assert res.status_code == status.HTTP_200_OK
    assert res.data['id'] == user.id
    assert res.data['username'] == user.username
