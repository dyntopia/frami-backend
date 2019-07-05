# pylint: disable=W0621
from pytest import fixture, mark
from rest_framework import status

from frami.api.models import Question

url = '/api/question/'
url_id = '/api/question/{}/'


@fixture
@mark.django_db
def questions(regular_user, extra_users):
    return {
        user: [
            Question.objects.create(
                user=user,
                subject='subject {} for {}'.format(i, user.username),
                message='message {} for {}'.format(i, user.username),
            ) for i in range(3)
        ]
        for user in [regular_user] + extra_users
    }


def test_create(api, regular_user):
    data = {
        'subject': 'some subject',
        'message': 'some message',
    }

    # Unauthenticated.
    res = api.post(url, data)
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Regular user.
    assert api.login(username=regular_user.username, password='password')
    res = api.post(url, data)
    assert res.status_code == status.HTTP_201_CREATED, res.data
    assert res.data['subject'] == data['subject']
    assert res.data['message'] == data['message']
    assert res.data['user'] == regular_user.username


def test_list(api, admin_user, regular_user, questions):
    # Unauthenticated.
    res = api.get(url)
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Regular user can list own questions.
    assert api.login(username=regular_user.username, password='password')
    res = api.get(url)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert len(res.data) == len(questions[regular_user])
    for i, q in enumerate(questions[regular_user]):
        assert res.data[i]['subject'] == q.subject
        assert res.data[i]['message'] == q.message
        assert res.data[i]['user'] == 'regular'

    # Admin can list all questions.
    assert api.login(username=admin_user.username, password='password')
    res = api.get(url)
    assert res.status_code == status.HTTP_200_OK, res.data
    assert len(res.data) == sum([len(q) for q in questions.values()])


def test_retrieve(api, admin_user, regular_user, extra_users, questions):
    # Unauthenticated.
    res = api.get(url_id.format(questions[regular_user][0].id))
    assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Users can retrieve their own questions.
    assert api.login(username=regular_user.username, password='password')
    for q in questions[regular_user]:
        res = api.get(url_id.format(q.id))
        assert res.status_code == status.HTTP_200_OK, res.data
        assert res.data['subject'] == q.subject
        assert res.data['message'] == q.message
        assert res.data['user'] == 'regular'

    # Users can not retrieve other users questions.
    for user in extra_users:
        for q in questions[user]:
            res = api.get(url_id.format(q.id))
            assert res.status_code == status.HTTP_403_FORBIDDEN, res.data

    # Admin can retrieve any question.
    assert api.login(username=admin_user.username, password='password')
    for user, qs in questions.items():
        for q in qs:
            res = api.get(url_id.format(q.id))
            assert res.status_code == status.HTTP_200_OK, res.data
            assert res.data['subject'] == q.subject
            assert res.data['message'] == q.message
            assert res.data['user'] == user.username
