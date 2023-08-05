from model_bakery import baker

from rest_framework.reverse import reverse

from utils.asserts import assert_status_created, assert_status_forbidden
from utils.helper import add_permission

from huscy.subjects.models import Address, Contact, Subject
from huscy.subjects.serializers import ContactSerializer


def test_admin_can_create_subject(admin_client):
    assert_status_created(create_subject(admin_client))


def test_user_with_permissions_can_create_subject(client, user):
    add_permission(user, 'add_subject')
    assert_status_created(create_subject(client))


def test_user_without_permissions_cannot_create_subject(client):
    assert_status_forbidden(create_subject(client))


def test_anonymous_cannot_create_subject(anonymous_client):
    assert_status_forbidden(create_subject(anonymous_client))


def test_address_contact_and_subject_created(client, user):
    add_permission(user, 'add_subject')

    assert not Address.objects.exists()
    assert not Contact.objects.exists()
    assert not Subject.objects.exists()

    create_subject(client)

    assert Address.objects.count() == 1
    assert Contact.objects.count() == 1
    assert Subject.objects.count() == 1


def create_subject(client):
    contact = baker.prepare('subjects.Contact', address=baker.prepare('subjects.Address'))

    data = {
        'contact': ContactSerializer(contact).data,
        'is_child': False,
        'is_patient': False,
    }
    return client.post(reverse('subject-list'), data=data, format='json')
