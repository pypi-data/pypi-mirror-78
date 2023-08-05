import pytest
from model_bakery import baker

from huscy.subjects.services import add_guardian

pytestmark = pytest.mark.django_db


def test_add_guardian(subject):
    contact = baker.make('subjects.Contact')

    assert subject.guardians.count() == 0

    add_guardian(subject, contact)

    assert list(subject.guardians.all()) == [contact]


def test_add_subject_itself_as_guardian(subject):
    assert subject.guardians.count() == 0

    with pytest.raises(ValueError) as e:
        add_guardian(subject, subject.contact)

    assert str(e.value) == 'Cannot add contact as guardian because it\'s the subject itself!'
    assert subject.guardians.count() == 0
