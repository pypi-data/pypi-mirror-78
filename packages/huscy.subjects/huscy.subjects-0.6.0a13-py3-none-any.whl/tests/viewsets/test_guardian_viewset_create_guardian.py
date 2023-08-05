import pytest
from model_bakery import baker

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN

from huscy.subjects.serializers import ContactSerializer

pytestmark = pytest.mark.django_db


def test_guardians_url(subject, guardian):
    url = reverse('guardian-list', kwargs=dict(subject_pk=subject.pk))
    assert url == f'/api/subjects/{subject.pk}/guardians/'


def test_admin_user_can_create_guardian(admin_client, subject):
    response = create_guardian(admin_client, subject)

    assert response.status_code == HTTP_201_CREATED, response.json()


def test_user_with_permission_can_create_guardian(client, user, subject):
    change_permission = Permission.objects.get(codename='change_subject')
    user.user_permissions.add(change_permission)

    response = create_guardian(client, subject)

    assert response.status_code == HTTP_201_CREATED, response.json()


def test_user_without_permission_cannot_create_guardian(client, subject):
    response = create_guardian(client, subject)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_create_guardian(anonymous_client, subject):
    response = create_guardian(anonymous_client, subject)

    assert response.status_code == HTTP_403_FORBIDDEN


def create_guardian(client, subject):
    contact = baker.prepare('subjects.Contact', address=baker.prepare('subjects.Address'))

    return client.post(
        reverse('guardian-list', kwargs=dict(subject_pk=subject.pk)),
        data=ContactSerializer(contact).data,
        format='json',
    )
