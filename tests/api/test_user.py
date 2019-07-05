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

    url = '/api/user/'

    # Forbidden.
    client.login(username='foo', password='bar')
    res = client.post(url, {'username': 'abc', 'password': 'pwpwpw1234'})
    assert res.status_code == status.HTTP_403_FORBIDDEN

    # New regular user.
    client.login(username='x', password='y')
    res = client.post(url, {'username': 'abc', 'password': 'pwpwpw1234'})
    assert not res.data['is_staff']
    assert res.data['username'] == 'abc'
    assert res.status_code == status.HTTP_201_CREATED
    assert client.login(username='abc', password='pwpwpw1234')

    # New staff.
    client.login(username='x', password='y')
    res = client.post(
        url, {
            'username': 'xyz',
            'password': 'pwpwpw1234',
            'is_staff': True,
        }
    )
    assert res.data['is_staff']
    assert res.data['username'] == 'xyz'
    assert res.status_code == status.HTTP_201_CREATED
    assert client.login(username='xyz', password='pwpwpw1234')

    # Duplicate.
    client.login(username='x', password='y')
    res = client.post(url, {'username': 'abc', 'password': 'pwpwpw1234'})
    assert 'unique' in [err.code for err in res.data['username']]
    assert res.status_code == status.HTTP_400_BAD_REQUEST

    # Missing password.
    client.login(username='x', password='y')
    res = client.post(url, {'username': 'meh'})
    assert 'required' in [err.code for err in res.data['password']]
    assert res.status_code == status.HTTP_400_BAD_REQUEST

    # Invalid password.
    client.login(username='x', password='y')
    res = client.post(url, {'username': 'meh', 'password': 'x'})
    assert 'password_too_short' in [err.code for err in res.data['password']]
    assert res.status_code == status.HTTP_400_BAD_REQUEST


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
    assert not res.data.get('password')


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
    assert not res.data.get('password')


@mark.django_db
def test_update(client):
    user = User.objects.create_user(username='foo', password='bar')
    other = User.objects.create_user(username='baz', password='qux')
    staff = User.objects.create_user(username='x', password='y', is_staff=True)

    user_url = '/api/user/{}/'.format(user.id)
    other_url = '/api/user/{}/'.format(other.id)
    staff_url = '/api/user/{}/'.format(staff.id)

    # User update other.
    client.login(username='foo', password='bar')
    res = client.patch(other_url, {'first_name': 'abc'}, 'application/json')
    assert res.status_code == status.HTTP_403_FORBIDDEN

    # User update self.
    client.login(username='foo', password='bar')
    res = client.patch(user_url, {'first_name': 'abc'}, 'application/json')
    assert res.status_code == status.HTTP_403_FORBIDDEN

    # Staff update other.
    client.login(username='x', password='y')
    res = client.patch(other_url, {'first_name': 'abc'}, 'application/json')
    assert res.status_code == status.HTTP_200_OK
    assert res.data['first_name'] == 'abc'

    # Staff update other with invalid password.
    client.login(username='x', password='y')
    res = client.patch(other_url, {'password': 'x'}, 'application/json')
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert 'password_too_short' in [err.code for err in res.data['password']]
    assert client.login(username='baz', password='qux')
    assert not client.login(username='baz', password='x')

    # Staff update other with valid password.
    client.login(username='x', password='y')
    res = client.patch(other_url, {'password': 'xyz43210'}, 'application/json')
    assert res.status_code == status.HTTP_200_OK
    assert client.login(username='baz', password='xyz43210')
    assert not client.login(username='baz', password='qux')

    # Staff update self.
    client.login(username='x', password='y')
    res = client.patch(staff_url, {'first_name': 'abc'}, 'application/json')
    assert res.status_code == status.HTTP_200_OK
    assert res.data['first_name'] == 'abc'

    # Staff update self with invalid password.
    client.login(username='x', password='y')
    res = client.patch(staff_url, {'password': 'x'}, 'application/json')
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert 'password_too_short' in [err.code for err in res.data['password']]
    assert client.login(username='x', password='y')
    assert not client.login(username='x', password='x')

    # Staff update self with valid password.
    client.login(username='x', password='y')
    res = client.patch(staff_url, {'password': 'xyz43210'}, 'application/json')
    assert res.status_code == status.HTTP_200_OK
    assert client.login(username='x', password='xyz43210')
    assert not client.login(username='x', password='y')
