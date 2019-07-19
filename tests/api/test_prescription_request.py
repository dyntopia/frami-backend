from rest_framework import status

from frami.api.models import Prescription, PrescriptionRequest

url = '/api/prescription-request/'
url_pk = '/api/prescription-request/{pk}/'


def test_create(api, admin_user, regular_user):
    prescription = Prescription.objects.create(
        medication='foo',
        quantity='bar',
        patient=regular_user,
        creator=admin_user,
    )

    # Unauthenticated.
    res = api.post(url, {'prescription': prescription.pk})
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Regular user can create.
    assert api.login(username=regular_user.username, password='password')
    res = api.post(url, {'prescription': prescription.pk})
    assert res.status_code == status.HTTP_201_CREATED, res.data

    # Staff cannot create.
    assert api.login(username=admin_user.username, password='password')
    res = api.post(url, {'prescription': prescription.pk})
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data


def test_destroy(api, admin_user, regular_user):
    prescription = Prescription.objects.create(
        medication='foo',
        quantity='bar',
        patient=regular_user,
        creator=admin_user,
    )
    prescription_request = PrescriptionRequest.objects.create(
        prescription=prescription,
        creator=regular_user,
    )

    # Unauthenticated.
    res = api.delete(url_pk.format(pk=prescription_request.pk))
    assert res.status_code == status.HTTP_403_FORBIDDEN

    # User cannot destroy.
    assert api.login(username=regular_user.username, password='password')
    res = api.delete(url_pk.format(pk=prescription_request.pk))
    assert res.status_code == status.HTTP_403_FORBIDDEN

    # Staff can destroy.
    assert api.login(username=admin_user.username, password='password')
    res = api.delete(url_pk.format(pk=prescription_request.pk))
    assert res.status_code == status.HTTP_204_NO_CONTENT
