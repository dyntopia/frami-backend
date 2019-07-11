from django.contrib.auth.models import Group
from pytest import mark, raises

from frami.api import groups


@mark.django_db
def test_invalid_group(mocker):
    mock = mocker.patch.object(groups, 'groups')
    mock.items.return_value = [['admin', ['abcd']]]
    with raises(groups.GroupError):
        groups.create_groups()


@mark.django_db
def test_valid_groups():
    before = list(Group.objects.all())
    groups.create_groups()
    after = list(Group.objects.all())
    assert len(after) > len(before)
