import pytest
from model_bakery import baker

from huscy.subjects.serializers import ContactSerializer, NoteSerializer, SubjectSerializer

pytestmark = pytest.mark.django_db


def test_expose_contact_data(subject):
    data = SubjectSerializer(subject).data

    assert data['contact'] == ContactSerializer(subject.contact).data


def test_expose_guardians(subject):
    guardians = baker.make('subjects.Contact', _quantity=2)
    subject.guardians.add(*guardians)
    subject.save()

    data = SubjectSerializer(subject).data

    assert data['guardians'] == ContactSerializer(guardians, many=True).data


def test_expose_empty_list_for_guardians_if_no_guardians_assigned(subject):
    data = SubjectSerializer(subject).data

    assert data['guardians'] == []


def test_is_child_is_exposed_as_false(subject):
    data = SubjectSerializer(subject).data

    assert data['is_child'] is False


def test_is_child_is_exposed_as_true(subject):
    baker.make('subjects.Child', subject=subject)

    data = SubjectSerializer(subject).data

    assert data['is_child'] is True


def test_is_patient_is_exposed_as_false(subject):
    data = SubjectSerializer(subject).data

    assert data['is_patient'] is False


def test_is_patient_is_exposed_as_true(subject):
    baker.make('subjects.Patient', subject=subject)

    data = SubjectSerializer(subject).data

    assert data['is_patient'] is True


def test_expose_notes(subject):
    notes = baker.make('subjects.Note', subject=subject, _quantity=2)

    data = SubjectSerializer(subject).data

    assert data['notes'] == NoteSerializer(notes, many=True).data


def test_expose_empty_list_for_notes_if_no_notes_exist(subject):
    data = SubjectSerializer(subject).data

    assert data['notes'] == []
