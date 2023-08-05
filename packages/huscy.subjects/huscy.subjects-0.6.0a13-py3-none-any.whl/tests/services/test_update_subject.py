import pytest

from huscy.subjects.services import update_subject

pytestmark = pytest.mark.django_db


def test_is_child_is_true(subject):
    assert subject.is_child is False

    update_subject(subject, is_child=True, is_patient=False)

    assert subject.is_child is True


def test_is_child_is_true_but_subject_is_already_a_child(child, subject):
    assert subject.is_child is True

    update_subject(subject, is_child=True, is_patient=False)

    assert subject.is_child is True


def test_is_child_is_false(subject):
    assert subject.is_child is False

    update_subject(subject, is_child=False, is_patient=False)

    assert subject.is_child is False


def test_is_child_is_false_but_subject_is_a_child(child, subject):
    assert subject.is_child is True

    update_subject(subject, is_child=False, is_patient=False)

    assert subject.is_child is False


def test_is_patient_is_true(subject):
    assert subject.is_patient is False

    update_subject(subject, is_child=False, is_patient=True)

    assert subject.is_patient is True


def test_is_patient_is_true_but_subject_is_already_a_patient(patient, subject):
    assert subject.is_patient is True

    update_subject(subject, is_child=False, is_patient=True)

    assert subject.is_patient is True


def test_is_patient_is_false(subject):
    assert subject.is_patient is False

    update_subject(subject, is_child=False, is_patient=False)

    assert subject.is_patient is False


def test_is_patient_is_false_but_subject_is_a_patient(patient, subject):
    assert subject.is_patient is True

    update_subject(subject, is_child=False, is_patient=False)

    assert subject.is_patient is False
