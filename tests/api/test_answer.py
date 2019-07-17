from rest_framework import status

from frami.api.models import Question

url = '/api/answer/'


def test_create(api, admin_user, regular_user):
    question = Question.objects.create(
        creator=regular_user,
        subject='foo',
        message='bar',
    )

    # Unauthenticated.
    res = api.post(url, {'message': 'baz', 'question': question.pk})
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Regular user.
    assert api.login(username=regular_user.username, password='password')
    res = api.post(url, {'message': 'baz', 'question': question.pk})
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Admin.
    assert api.login(username=admin_user.username, password='password')
    res = api.post(url, {'message': 'baz', 'question': question.pk})
    assert res.status_code == status.HTTP_201_CREATED, res.data
    assert res.data['message'] == 'baz'
    assert res.data['question'] == question.pk
    assert res.data['creator'] == admin_user.username

    # Admin, missing question.
    assert api.login(username=admin_user.username, password='password')
    res = api.post(url, {'message': 'baz'})
    assert res.status_code == status.HTTP_400_BAD_REQUEST, res.data
    assert 'required' in [err.code for err in res.data['question']]

    # Admin, invalid question.
    assert api.login(username=admin_user.username, password='password')
    res = api.post(url, {'message': 'baz', 'question': 9999})
    assert res.status_code == status.HTTP_400_BAD_REQUEST, res.data
    assert 'does_not_exist' in [err.code for err in res.data['question']]
