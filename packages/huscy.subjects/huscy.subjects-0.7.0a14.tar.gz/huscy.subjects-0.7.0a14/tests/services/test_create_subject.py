import pytest

from huscy.subjects.services import create_subject

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize('is_child', [True, False])
def test_is_child(contact, is_child):
    subject = create_subject(contact, is_child=is_child)

    assert subject.is_child is is_child


@pytest.mark.parametrize('is_patient', [True, False])
def test_is_patient(contact, is_patient):
    subject = create_subject(contact, is_patient=is_patient)

    assert subject.is_patient is is_patient
