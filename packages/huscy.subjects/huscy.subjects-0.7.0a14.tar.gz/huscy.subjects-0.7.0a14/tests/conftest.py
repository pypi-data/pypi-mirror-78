import os
import pytest
import random
import string
import sys

from model_bakery import baker
from rest_framework.test import APIClient


# to import utils module in tests we need this:
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))


# model_bakery does not know how to deal with phonenumber-field, hence we provide some custom values
def gen_phonenumber():
    return '+4930' + ''.join(random.choices(string.digits, k=6))


baker.generators.add('phonenumber_field.modelfields.PhoneNumberField', gen_phonenumber)


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username='user', password='password',
                                                 first_name='Donna', last_name='Wetter')


@pytest.fixture
def client(user):
    client = APIClient()
    client.login(username=user.username, password='password')
    return client


@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    client.login(username=admin_user.username, password='password')
    return client


@pytest.fixture
def anonymous_client():
    return APIClient()


@pytest.fixture
def address(contact):
    return baker.make('subjects.Address', street='A Street 4', zip_code='00700', country='DE',
                      city='Bielefeld', contact=contact)


@pytest.fixture
def contact():
    return baker.make('subjects.Contact', display_name='John Doe', first_name='John',
                      last_name='Doe', email='john.doe@do.es')


@pytest.fixture
def subject(contact):
    return baker.make('subjects.Subject', contact=contact)


@pytest.fixture
def child(subject):
    return baker.make('subjects.Child', subject=subject)


@pytest.fixture
def patient(subject):
    return baker.make('subjects.Patient', subject=subject)


@pytest.fixture
def guardian(subject):
    contact = baker.make('subjects.Contact')
    subject.guardians.add(contact)
    return contact


@pytest.fixture
def note(subject):
    return baker.make('subjects.Note', subject=subject)


@pytest.fixture
def inactivity(subject):
    return baker.make('subjects.Inactivity', subject=subject)
