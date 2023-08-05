import pytest

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN

pytestmark = pytest.mark.django_db


def test_notes_url(subject, note):
    url = reverse('note-detail', kwargs=dict(pk=note.pk, subject_pk=subject.pk))
    assert url == f'/api/subjects/{subject.pk}/notes/{note.pk}/'


def test_admin_user_can_remove_note(admin_client, subject, note):
    response = remove_note(admin_client, subject, note)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_user_with_permission_can_remove_note(client, user, subject, note):
    change_permission = Permission.objects.get(codename='change_subject')
    user.user_permissions.add(change_permission)

    response = remove_note(client, subject, note)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_user_without_permission_cannot_remove_note(client, subject, note):
    response = remove_note(client, subject, note)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_remove_note(anonymous_client, subject, note):
    response = remove_note(anonymous_client, subject, note)

    assert response.status_code == HTTP_403_FORBIDDEN


def remove_note(client, subject, note):
    return client.delete(
        reverse('note-detail', kwargs=dict(pk=note.pk, subject_pk=subject.pk))
    )
