from rest_framework import status

from frami.api.models import Prescription


def test_unauthenticated(client, regular_user):
    user = regular_user.id

    assert client.get('/api/prescription/').status_code == \
        status.HTTP_403_FORBIDDEN
    assert client.get('/api/prescription/{}/'.format(user)).status_code == \
        status.HTTP_403_FORBIDDEN


def test_create(api, admin_user, regular_user):
    url = '/api/prescription/'
    data = {
        'medication': 'foo',
        'quantity': 'bar',
        'user': regular_user.pk,
    }

    # regular
    api.login(username='admin', password='password')
    res = api.post(url, data)
    assert res.status_code == status.HTTP_201_CREATED

    # admin
    api.login(username='admin', password='password')
    res = api.post(url, data)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.data['medication'] == 'foo'
    assert res.data['quantity'] == 'bar'
    assert res.data['user'] == regular_user.pk
    assert res.data['prescriber'] == admin_user.username


def test_destroy(api, admin_user, regular_user):
    prescription = Prescription.objects.create(
        medication='foo',
        quantity='bar',
        user=regular_user,
        prescriber=admin_user,
    )
    url = '/api/prescription/{}/'.format(prescription.pk)

    # regular
    api.login(username='regular', password='password')
    assert api.delete(url).status_code == status.HTTP_403_FORBIDDEN

    # admin
    api.login(username='admin', password='password')
    assert api.delete(url).status_code == status.HTTP_204_NO_CONTENT
    assert api.get(url).status_code == status.HTTP_404_NOT_FOUND


def test_retrieve(api, admin_user, regular_user):
    prescription = Prescription.objects.create(
        medication='foo',
        quantity='bar',
        user=regular_user,
        prescriber=admin_user,
    )
    url = '/api/prescription/{}/'.format(prescription.pk)

    # regular
    api.login(username='regular', password='password')
    assert api.get(url).status_code == status.HTTP_403_FORBIDDEN

    # admin
    api.login(username='admin', password='password')
    res = api.get(url)
    assert res.status_code == status.HTTP_200_OK
    assert res.data['medication'] == 'foo'
    assert res.data['quantity'] == 'bar'
    assert res.data['user'] == regular_user.pk
    assert res.data['prescriber'] == admin_user.username


def test_update(api, admin_user, regular_user):
    prescription = Prescription.objects.create(
        medication='foo',
        quantity='bar',
        user=regular_user,
        prescriber=admin_user,
    )
    partial = {
        'medication': 'baz',
    }
    full = {
        'medication': 'qux',
        'quantity': 'abc',
        'user': regular_user.pk,
        'prescriber': admin_user.username,
    }
    url = '/api/prescription/{}/'.format(prescription.pk)

    # regular, partial
    api.login(username='regular', password='password')
    assert api.patch(url, partial).status_code == status.HTTP_403_FORBIDDEN

    # regular, full
    api.login(username='regular', password='password')
    assert api.put(url, full).status_code == status.HTTP_403_FORBIDDEN

    # admin, partial
    api.login(username='admin', password='password')
    res = api.patch(url, partial)
    assert res.status_code == status.HTTP_200_OK
    assert res.data['medication'] == 'baz'
    assert res.data['quantity'] == 'bar'
    assert res.data['user'] == regular_user.pk
    assert res.data['prescriber'] == admin_user.username

    # admin, full
    api.login(username='admin', password='password')
    res = api.put(url, full)
    assert res.status_code == status.HTTP_200_OK
    assert res.data['medication'] == 'qux'
    assert res.data['quantity'] == 'abc'
    assert res.data['user'] == regular_user.pk
    assert res.data['prescriber'] == admin_user.username


def test_on_user_delete(admin_user, regular_user):
    Prescription.objects.create(
        medication='foo',
        quantity='bar',
        user=regular_user,
        prescriber=admin_user,
    )

    assert Prescription.objects.all()
    regular_user.delete()
    assert not Prescription.objects.all()


def test_on_prescriber_delete(admin_user, regular_user):
    Prescription.objects.create(
        medication='foo',
        quantity='bar',
        user=regular_user,
        prescriber=admin_user,
    )

    assert len(Prescription.objects.all()) == 1
    admin_user.delete()
    assert Prescription.objects.first().prescriber.username == 'deleted'
