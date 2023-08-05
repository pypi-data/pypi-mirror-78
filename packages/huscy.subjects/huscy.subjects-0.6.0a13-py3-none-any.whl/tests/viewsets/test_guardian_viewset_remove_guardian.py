import pytest

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN

pytestmark = pytest.mark.django_db


def test_guardians_url(subject, guardian):
    url = reverse('guardian-detail', kwargs=dict(pk=guardian.pk, subject_pk=subject.pk))
    assert url == f'/api/subjects/{subject.pk}/guardians/{guardian.pk}/'


def test_admin_user_can_remove_guardian(admin_client, subject, guardian):
    response = remove_guardian(admin_client, subject, guardian)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_user_with_permission_can_remove_guardian(client, user, subject, guardian):
    change_permission = Permission.objects.get(codename='change_subject')
    user.user_permissions.add(change_permission)

    response = remove_guardian(client, subject, guardian)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_user_without_permission_cannot_remove_guardian(client, subject, guardian):
    response = remove_guardian(client, subject, guardian)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_remove_guardian(anonymous_client, subject, guardian):
    response = remove_guardian(anonymous_client, subject, guardian)

    assert response.status_code == HTTP_403_FORBIDDEN


def remove_guardian(client, subject, guardian):
    return client.delete(
        reverse('guardian-detail', kwargs=dict(pk=guardian.pk, subject_pk=subject.pk))
    )
