import pytest
from model_bakery import baker

from huscy.subjects.models import Contact
from huscy.subjects.services import remove_guardian

pytestmark = pytest.mark.django_db


def test_guardian_has_subject(subject, guardian):
    assert subject.guardians.count() == 1
    assert guardian.subjects.count() == 1

    remove_guardian(subject, guardian)

    assert subject.guardians.count() == 0
    assert not Contact.objects.filter(pk=guardian.pk).exists()


def test_guardian_has_multiple_subjects(subject, guardian):
    another_subject = baker.make('subjects.Subject')
    another_subject.guardians.add(guardian)

    assert subject.guardians.count() == 1
    assert another_subject.guardians.count() == 1
    assert guardian.subjects.count() == 2

    remove_guardian(subject, guardian)

    assert subject.guardians.count() == 0
    assert another_subject.guardians.count() == 1
    assert guardian.subjects.count() == 1
    assert Contact.objects.filter(pk=guardian.pk).exists()
