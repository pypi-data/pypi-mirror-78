import pytest

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

pytestmark = pytest.mark.django_db


def test_get_notes_url(subject):
    url = reverse('note-list', kwargs=dict(subject_pk=subject.pk))
    assert url == f'/api/subjects/{subject.pk}/notes/'


def test_admin_user_can_get_notes(admin_client, subject):
    response = get_notes(admin_client, subject)

    assert response.status_code == HTTP_200_OK


def test_user_with_permission_can_get_notes(client, user, subject):
    change_permission = Permission.objects.get(codename='change_subject')
    user.user_permissions.add(change_permission)

    response = get_notes(client, subject)

    assert response.status_code == HTTP_200_OK, response.json()


def test_user_without_permission_cannot_get_notes(client, subject):
    response = get_notes(client, subject)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_get_notes(anonymous_client, subject):
    response = get_notes(anonymous_client, subject)

    assert response.status_code == HTTP_403_FORBIDDEN


def get_notes(client, subject):
    return client.get(
        reverse('note-list', kwargs=dict(subject_pk=subject.pk)),
    )
