from rest_framework import status

url = '/api/result/'
url_pk = '/api/result/{pk}/'
url_patient = '/api/result/?patient={patient}'


def test_create(api, admin_user, regular_user):
    data = {
        'kind': 'lab report',
        'result': 'text...',
        'patient': regular_user.pk,
    }

    # Unauthenticated.
    res = api.post(url, data)
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Regular user.
    assert api.login(username=regular_user.username, password='password')
    res = api.post(url, data)
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Admin.
    assert api.login(username=admin_user.username, password='password')
    res = api.post(url, data)
    assert res.status_code == status.HTTP_201_CREATED, res.data
    assert res.data['kind'] == data['kind']
    assert res.data['result'] == data['result']
    assert res.data['patient'] == regular_user.pk
    assert res.data['creator'] == admin_user.username


def test_destroy(api, admin_user, regular_user, results):
    target = url_pk.format(pk=results[regular_user][0].pk)

    # Unauthenticated.
    assert api.delete(target).status_code == status.HTTP_403_FORBIDDEN

    # Regular user.
    assert api.login(username=regular_user.username, password='password')
    assert api.delete(target).status_code == status.HTTP_403_FORBIDDEN
    assert api.get(target).status_code == status.HTTP_200_OK

    # Admin.
    assert api.login(username=admin_user.username, password='password')
    assert api.delete(target).status_code == status.HTTP_204_NO_CONTENT
    assert api.get(target).status_code == status.HTTP_404_NOT_FOUND


def test_list(api, admin_user, regular_user, results):
    # Unauthenticated.
    res = api.get(url)
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Regular user can list own results.
    assert api.login(username=regular_user.username, password='password')
    res = api.get(url)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert len(res.data) == len(results[regular_user])
    for i, r in enumerate(results[regular_user]):
        assert res.data[i]['kind'] == r.kind
        assert res.data[i]['result'] == r.result
        assert res.data[i]['patient'] == regular_user.pk

    # Admin can list all results.
    assert api.login(username=admin_user.username, password='password')
    res = api.get(url)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert len(res.data) == sum([len(r) for r in results.values()])

    # Admin can retrieve a list of filtered results.
    assert api.login(username=admin_user.username, password='password')
    res = api.get(url_patient.format(patient=regular_user.pk))
    assert res.status_code == status.HTTP_200_OK, res.data
    assert len(res.data) == len(results[regular_user])
    for i, r in enumerate(results[regular_user]):
        assert res.data[i]['kind'] == r.kind
        assert res.data[i]['result'] == r.result
        assert res.data[i]['patient'] == regular_user.pk


def test_retrieve(api, admin_user, regular_user, extra_users, results):
    # Unauthenticated.
    res = api.get(url_pk.format(pk=results[regular_user][0].pk))
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Regular user can retrieve their own results.
    assert api.login(username=regular_user.username, password='password')
    for r in results[regular_user]:
        res = api.get(url_pk.format(pk=r.pk))
        assert res.status_code == status.HTTP_200_OK, res.data
        assert res.data['kind'] == r.kind
        assert res.data['result'] == r.result
        assert res.data['patient'] == regular_user.pk

    # Users can not retrieve other users results.
    for user in extra_users:
        for r in results[user]:
            res = api.get(url_pk.format(pk=r.pk))
            assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Admin can retrieve any result.
    assert api.login(username=admin_user.username, password='password')
    for user, rs in results.items():
        for r in rs:
            res = api.get(url_pk.format(pk=r.pk))
            assert res.status_code == status.HTTP_200_OK, res.data
            assert res.data['kind'] == r.kind
            assert res.data['result'] == r.result
            assert res.data['patient'] == user.pk


def test_update(api, admin_user, regular_user, extra_users, results):
    result = results[regular_user][0]
    partial = {
        'kind': result.kind + ' partial update',
    }
    full = {
        'kind': result.kind + ' full update',
        'result': result.result + ' full update',
        'patient': result.patient.pk,
        'creator': extra_users[0].username,
    }

    # Unauthenticated, partial.
    res = api.patch(url_pk.format(pk=result.pk), partial)
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Unauthenticated, full.
    res = api.put(url_pk.format(pk=result.pk), full)
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Regular user, partial.
    assert api.login(username=regular_user.username, password='password')
    res = api.patch(url_pk.format(pk=result.pk), partial)
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Regular user, full.
    assert api.login(username=regular_user.username, password='password')
    res = api.put(url_pk.format(pk=result.pk), full)
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Admin, partial.
    assert api.login(username=admin_user.username, password='password')
    res = api.patch(url_pk.format(pk=result.pk), partial)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert res.data['kind'] == partial['kind']
    assert res.data['result'] == result.result
    assert res.data['patient'] == result.patient.pk
    assert res.data['creator'] == admin_user.username

    # Admin, full
    assert api.login(username=admin_user.username, password='password')
    res = api.put(url_pk.format(pk=result.pk), full)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert res.data['kind'] == full['kind']
    assert res.data['result'] == full['result']
    assert res.data['patient'] == full['patient']
    assert res.data['creator'] == admin_user.username
